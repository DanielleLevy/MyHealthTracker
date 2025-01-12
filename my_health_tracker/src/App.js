import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./loginPage/LoginPage";
import MainPage from "./MainPage";

function App() {
  return (
    <Router>
      <Routes>
        {/* ניתוב לעמוד ה-Login */}
        <Route path="/" element={<LoginPage />} />
        {/* ניתוב לעמוד ה-MainPage */}
        <Route path="/mainpage" element={<MainPage />} />
      </Routes>
    </Router>
  );
}

export default App;
