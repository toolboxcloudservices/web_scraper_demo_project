import os

# Directory for storing screenshots
SCREENSHOT_DIR = "static/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Directory for storing generated reports
UPLOAD_FOLDER = 'generated_reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
