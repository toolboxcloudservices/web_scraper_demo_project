
# Web Scraper Frontend (React)

This is the frontend of a Web Scraping project built using **React**, which communicates with a **Python Flask** backend. The scraper extracts valuable IT department contact information from town/city websites, processes it, and generates reports. The frontend provides an interactive interface for users to input websites, start scraping, and view the results.

## Project Overview

The frontend of the web scraper is built using **React** and styled using **Ant Design**. The application provides a clean UI for users to input a URL, start the scraping process, view progress, and download the generated report.

### Key Features:
- Input a URL and start the scraping process.
- Display the scraping progress with steps.
- View scraping results in a structured format.
- Download reports as `.xls` files.
- View screenshots taken during scraping.

## Technologies Used:
- **React**: For building the user interface.
- **Ant Design**: For UI components and styling.
- **React Router**: For page navigation.
- **Axios**: For making HTTP requests to the backend (Python Flask).
- **React Icons**: For adding icons to the UI.

## Setup and Installation

To run the frontend locally, follow the steps below:

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/web-scraper-frontend.git
cd web-scraper-frontend
```

### 2. Install dependencies

Make sure you have **Node.js** and **npm** (or **yarn**) installed. Then, run the following command to install the dependencies:

```bash
npm install
```

### 3. Run the development server

After the dependencies are installed, you can start the development server by running:

```bash
npm start
```

This will start the frontend on [http://localhost:3000](http://localhost:3000).

## Available Scripts

In the project directory, you can run the following commands:

### `npm start`

Runs the app in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### `npm test`

Launches the test runner in the interactive watch mode.

### `npm run build`

Builds the app for production to the `build` folder.

### `npm run eject`

Removes the single build dependency from the project.

## Project Structure

```bash
src/
  assets/                  # Static assets like images and icons
  components/              # Reusable components (Form, Logs, Screenshots)
  pages/                   # Individual pages (e.g. Home, Scraper)
  App.js                   # Main app component
  index.js                 # Entry point of the app
public/
  index.html               # Main HTML template
  logo.png                 # App logo
```
