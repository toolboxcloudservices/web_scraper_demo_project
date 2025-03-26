import os
import re
import time
import logging
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
from flask import Flask, request, send_from_directory, Response, send_file, jsonify
from flask_cors import CORS, cross_origin
from config import SCREENSHOT_DIR

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # If your frontend is on port 3000

# Logging setup
log_stream = StringIO()
handler = logging.StreamHandler(log_stream)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Configuration for different sites
configurations = {
    "chatham-ma.gov": {
        "base_url": "https://www.chatham-ma.gov",
        "departments_keywords": ["departments"],
        "it_department_keywords": ["information technology", "it department", "tech support", "technical services", "technology"],
        "contact_info_selectors": {
            "container": "li.widgetItem.h-card",
            "name": "h4.widgetTitle.field.p-name",
            "title": "div.field.p-job-title",
            "phone": "div.field.p-tel a",
            "email": "div.field.u-email a",
            "address": "div.field.h-adr"
        },
        "dynamic_patterns": ["contact", "info", "department"]
    },
    "ashlandmass.com": {
        "base_url": "https://www.ashlandmass.com",
        "departments_keywords": ["departments"],
        "it_department_keywords": ["information technology", "it department", "tech support", "technical services", "technology"],
        "contact_info_selectors": {
            "container": "li.widgetItem.h-card",
            "name": "h4.widgetTitle.field.p-name",
            "title": "div.field.p-job-title",
            "phone": "div.field.p-tel a",
            "email": "div.field.u-email a",
            "address": "div.field.h-adr"
        },
        "dynamic_patterns": ["contact", "info", "department"]
    }
}


def get_config_by_url(url):
    """
    Retrieves the configuration settings for a given URL.

    Args:
        url (str): The website URL to match against known configurations.

    Returns:
        dict or None: Returns the matching configuration dictionary if found, otherwise None.
    """
    for key in configurations.keys():
        if key in url:
            return configurations[key]
    return None


def log_info(message):
    """
    Logs informational messages using the Flask application's logger.

    Args:
        message (str): The message to log.
    """
    app.logger.info(message)


def sanitize_url(url):
    """
    Validates and sanitizes a given URL to ensure it starts with 'http' or 'https'.

    Args:
        url (str): The URL to sanitize.

    Returns:
        str or None: Returns the sanitized URL if valid, otherwise None.
    """
    if not re.match(r'^https?://', url):
        return None
    return url


def capture_screenshot(url, step):
    """
    Captures a screenshot of a given URL using Selenium's WebDriver.

    Args:
        url (str): The webpage URL to capture.
        step (str): A descriptive name for the screenshot file.

    Returns:
        str: The file path of the saved screenshot.
    """
    service = ChromeService(executable_path=binary_path)
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")  # Optional: useful for debugging

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"screenshot_{step}.png")
        driver.save_screenshot(screenshot_path)
    finally:
        driver.quit()

    return screenshot_path


def extract_emails_and_phones(text):
    """
    Extracts email addresses and phone numbers from a given text.

    Args:
        text (str): The text content to search.

    Returns:
        tuple: A tuple containing two lists - extracted emails and phone numbers.
    """
    log_info("Extracting emails and phone numbers...")

    # Regex pattern for extracting emails
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)

    # Regex pattern for extracting phone numbers in formats like (123) 456-7890, 123-456-7890, 123.456.7890
    phones = re.findall(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', text)

    log_info(f"Found {len(emails)} emails and {len(phones)} phone numbers.")
    return emails, phones


def find_links_with_keywords(soup, keywords, base_url):
    """
    Finds links on a webpage that contain specified keywords in either the text or the URL.

    Args:
        soup (BeautifulSoup): The parsed HTML content of the page.
        keywords (list): A list of keywords to search for in links.
        base_url (str): The base URL to resolve relative links.

    Returns:
        list: A list of full URLs matching the given keywords.
    """
    log_info("Searching for links with keywords...")
    links = []

    for a_tag in soup.find_all('a', href=True):
        link_text = a_tag.get_text(strip=True).lower()
        href = a_tag['href'].lower()

        log_info(f"Checking link: text='{link_text}', href='{href}'")

        # Check if any keyword is found in the link text or href
        if any(keyword.lower() in link_text for keyword in keywords) or any(keyword.lower() in href for keyword in keywords):
            log_info(f"Match found: text='{link_text}', href='{href}'")

            # Convert relative URLs to absolute URLs
            full_url = href
            if not href.startswith("http"):
                full_url = f"{base_url}{href}"
            links.append(full_url)

    log_info(f"Total {len(links)} links found with specified keywords.")
    return links


def dynamic_contact_detection(soup):
    """
    Dynamically detects contact information on a webpage by searching for class and ID patterns.

    Args:
        soup (BeautifulSoup): The parsed HTML content.

    Returns:
        list: A list of detected contact information dictionaries containing text content, emails, and phone numbers.
    """
    log_info("Attempting dynamic contact information detection...")
    potential_contacts = []

    # Look for elements that match predefined dynamic class or ID patterns
    for pattern in configurations["dynamic_patterns"]:
        elements = soup.find_all(class_=lambda class_name: class_name and pattern in class_name.lower())
        elements += soup.find_all(id=lambda id_name: id_name and pattern in id_name.lower())
        potential_contacts.extend(elements)

    unique_contacts = list(set(potential_contacts))
    contacts_data = []

    for contact in unique_contacts:
        text_content = contact.get_text(separator=" ", strip=True)
        emails, phones = extract_emails_and_phones(text_content)
        log_info(f"Dynamic detection found: {text_content}")

        contacts_data.append({
            "Content": text_content,
            "Emails": emails,
            "Phones": phones
        })

    return contacts_data


def scrape_it_department_data(url):
    """
    Scrapes IT department contact information from a given website.

    This function navigates through a municipal or organizational website to locate
    the IT department page, extract relevant links, and scrape contact details such
    as names, titles, phone numbers, and email addresses.

    Args:
        url (str): The base URL of the website to scrape.

    Returns:
        list: A list of dictionaries containing IT department contact information.
    """

    # Retrieve the configuration for the provided URL
    selected_config = get_config_by_url(url)
    if not selected_config:
        log_info(f"No configuration found for the URL: {url}")
        return []

    # Extract configuration details
    base_url = selected_config["base_url"]
    departments_keywords = selected_config["departments_keywords"]
    it_department_keywords = selected_config["it_department_keywords"]
    contact_info_selectors = selected_config["contact_info_selectors"]

    it_data = []

    # Initialize the Selenium WebDriver
    log_info(f"Initializing Selenium WebDriver for URL: {url}")
    service = ChromeService(executable_path=binary_path)
    options = Options()
    options.headless = True  # Run in headless mode (no UI)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Visit the main page
        log_info("Navigating to the main page...")
        driver.get(url)

        # Wait until the page loads completely
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        rendered_html = driver.page_source
        log_info("Main page loaded successfully.")

        # Capture a screenshot for debugging or verification
        capture_screenshot(url, "main_page")

        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(rendered_html, 'html.parser')

        # Locate the "Departments" page link
        log_info("Searching for the 'Departments' link...")
        departments_link = None

        for a_tag in soup.find_all('a', href=True):
            link_text = a_tag.get_text(strip=True).lower()
            href = a_tag['href'].lower()

            # Check if the link text or URL contains department-related keywords
            if any(keyword in link_text for keyword in departments_keywords) or \
                    any(keyword in href for keyword in departments_keywords):
                departments_link = a_tag['href']

                # Convert relative URL to absolute URL if necessary
                if not departments_link.startswith("http"):
                    departments_link = f"{base_url}{departments_link}"

                log_info(f"'Departments' link found: {departments_link}")
                break

        if not departments_link:
            log_info("No 'Departments' link found.")
            return []

        # Visit the 'Departments' page
        log_info(f"Navigating to the 'Departments' page: {departments_link}")
        driver.get(departments_link)

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        rendered_html = driver.page_source
        log_info("'Departments' page loaded successfully.")

        # Capture a screenshot of the departments page
        capture_screenshot(departments_link, "departments_page")

        # Parse the content of the 'Departments' page
        soup = BeautifulSoup(rendered_html, 'html.parser')

        # Search for links related to IT departments
        log_info("Searching for IT-related links on the 'Departments' page...")
        it_links = find_links_with_keywords(soup, it_department_keywords, base_url)
        log_info(f"Found {len(it_links)} links related to IT department.")

        visited_links = set()

        # Loop through each identified IT-related link and extract contact details
        for link in it_links:
            if link in visited_links:
                log_info(f"Skipping duplicate link: {link}")
                continue

            visited_links.add(link)

            log_info(f"Navigating to IT department page: {link}")
            driver.get(link)

            # Wait for the IT department page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            rendered_html = driver.page_source
            log_info("IT department page loaded successfully.")

            # Capture a screenshot of the IT department page
            capture_screenshot(link, "it_department_page")

            # Parse the IT department page content
            soup = BeautifulSoup(rendered_html, 'html.parser')

            # Extract contact details from the page
            log_info("Extracting data from the IT department page...")
            for item in soup.select(contact_info_selectors["container"]):
                name = item.select_one(contact_info_selectors["name"]).get_text(strip=True) if item.select_one(
                    contact_info_selectors["name"]) else "N/A"
                title = item.select_one(contact_info_selectors["title"]).get_text(strip=True) if item.select_one(
                    contact_info_selectors["title"]) else "N/A"
                phone = item.select_one(contact_info_selectors["phone"]).get_text(strip=True) if item.select_one(
                    contact_info_selectors["phone"]) else "N/A"
                email = item.select_one(contact_info_selectors["email"]).get('href', 'N/A').replace('mailto:',
                                                                                                    '') if item.select_one(
                    contact_info_selectors["email"]) else "N/A"
                address = item.select_one(contact_info_selectors["address"]).get_text(strip=True).replace('\n',
                                                                                                          ', ') if item.select_one(
                    contact_info_selectors["address"]) else "N/A"

                # Log the extracted contact information
                log_info(f"Found contact: Name={name}, Title={title}, Phone={phone}, Email={email}, Address={address}")

                # Append extracted contact details to the results list
                it_data.append({
                    "Town URL": url,
                    "Town Name": base_url.split("//")[1].split(".")[0].capitalize(),
                    "Department": "Information Technology",
                    "Name": name,
                    "Title": title,
                    "Phone": phone,
                    "Email": email,
                    "Address": address
                })

    finally:
        # Ensure the driver is properly closed
        driver.quit()

    return it_data

# Route to handle IT department data scraping
@app.route('/api', methods=['POST'])
def index():
    data = request.json  # Expecting JSON request body
    url = data.get("url")  # Extract URL from request

    sanitized_url = sanitize_url(url)
    if not sanitized_url:
        return jsonify({"error": "Invalid URL"}), 400  # Return error response if URL is invalid

    extracted_data = scrape_it_department_data(sanitized_url)

    if not extracted_data:
        return jsonify({"message": "No IT contact information found."}), 404  # No data found

    # Save extracted data as an Excel report
    output_filename = "IT_Department_Data_Report.xlsx"
    df = pd.DataFrame(extracted_data)
    df.to_excel(output_filename, index=False)

    # Just for debugging, log the response
    response_data = {
        "data": extracted_data,
        "report_url": f"http://127.0.0.1:5000/download/{output_filename}",
        "screenshots": ["main_page", "departments_page", "it_department_page"]
    }
    print(response_data)  # Log to check the response structure

    return jsonify(response_data)


# Route to provide real-time log streaming
@app.route('api/logs')
@cross_origin
def logs():
    """
    Streams real-time log updates to the client.

    This endpoint allows the frontend to receive live updates from the log stream.
    It continuously checks for new log content and sends it as a Server-Sent Event (SSE).

    Returns:
        Server-Sent Event (SSE) response containing real-time log data.
    """
    def generate():
        log_stream.seek(0)  # Move to the beginning of the log stream
        while True:
            time.sleep(1)  # Wait for new log updates
            log_content = log_stream.getvalue()  # Retrieve current log content
            log_stream.truncate(0)  # Clear log stream after sending
            log_stream.seek(0)

            if log_content:
                yield f"data:{log_content}\n\n"  # Send log data as SSE
            else:
                yield ": keep-alive\n\n"  # Send keep-alive message if no new logs

    return Response(generate(), mimetype='text/event-stream')



# Route to allow downloading of generated reports
@app.route('/download/<filename>')
def download_file(filename):
    """
    Serves the requested file for download.
    """
    return send_from_directory(os.getcwd(), filename)  # Serve the requested file



# Route to retrieve screenshots taken during the scraping process
@app.route('/screenshot/<step>')
def get_screenshot(step):
    """
    Serves a screenshot taken at a specific step in the scraping process.
    """
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"screenshot_{step}.png")
    if os.path.exists(screenshot_path):
        return send_file(screenshot_path, mimetype='image/png')  # Serve the screenshot
    return "Screenshot not found", 404  # Return error if screenshot is missing


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
