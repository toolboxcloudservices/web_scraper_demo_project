import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import WelcomePage from "./components/WelcomePage";
import ScraperPage from "./components/ScraperPage"; // Your scraper component

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<WelcomePage />} />
        <Route path="/scraper" element={<ScraperPage />} />
      </Routes>
    </Router>
  );
}

export default App;
