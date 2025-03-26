# IT Department Scraping API

This project is a backend service that scrapes IT department contact information from provided URLs. It uses Selenium for dynamic page rendering and BeautifulSoup for extracting data. The extracted information is returned as structured JSON data, and you can also download it as an Excel report. Screenshots of the page steps are also provided.

## Features
- **Scrape IT Department Contact Info**: Extracts relevant IT department contact details (name, title, phone, email, and address).
- **Screenshot Generation**: Captures screenshots of different stages during the scraping process.
- **Excel Report**: Converts the scraped data into an Excel report that can be downloaded.
- **Log Streaming**: Real-time log streaming for debugging purposes.

## Prerequisites

Make sure you have the following installed:
- Python 3.7 or higher
- Chrome WebDriver (for Selenium)
- Google Chrome browser

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/toolboxcloudservices/web_scraper_demo_project.git
    cd back_end
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure the `chromedriver` executable is available in your environment's PATH or provide its path in the code.

4. Start the application:
    ```bash
    python app.py
    ```

5. The API will be available at `http://127.0.0.1:5000/`.

## API Endpoints

### 1. `/` (POST)
- **Description**: Scrapes the IT department contact information for the provided URL.
- **Request Body**: 
    ```json
    {
        "url": "https://www.chatham-ma.gov.com"
    }
    ```
- **Response**: 
    - **200 OK**: If data is found.
    - **400 Bad Request**: If the URL is invalid.
    - **404 Not Found**: If no IT department contact information is found.
    - Returns:
      ```json
      {
          "data": [
              {
                  "Town URL": "https://example.com",
                  "Town Name": "Example",
                  "Department": "Information Technology",
                  "Name": "John Doe",
                  "Title": "IT Manager",
                  "Phone": "123-456-7890",
                  "Email": "johndoe@example.com",
                  "Address": "123 Main St, Example City, EX"
              }
          ],
          "report_url": "http://127.0.0.1:5000/download/IT_Department_Data_Report.xlsx",
          "screenshots": [
              "main_page",
              "departments_page",
              "it_department_page"
          ]
      }
      ```

### 2. `/logs` (GET)
- **Description**: Streams the real-time logs of the application.
- **Response**: 
    - Returns logs as a server-sent event stream.

### 3. `/download/<filename>` (GET)
- **Description**: Downloads the generated report file.
- **Response**: 
    - Returns the file in the response for download.

### 4. `/screenshot/<step>` (GET)
- **Description**: Retrieves a screenshot taken at a specific step during scraping.
- **Response**: 
    - Returns the screenshot image if found.
    - Returns "Screenshot not found" if the screenshot doesn't exist.

## Running Tests

To run tests, you need to install `pytest` and execute the tests with the following command:

```bash
pip install pytest
pytest
