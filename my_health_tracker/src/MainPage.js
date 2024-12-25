import React, { useState } from "react";
import "./MainPage.css";
import logo from './loginPage/welcome/logo.png';  // Import SVG as a React component


function MainPage() {
    const [showReminders, setShowReminders] = useState(false);
  
    const handleRemindersClick = () => {
      setShowReminders(!showReminders);
    };
  
    return (
      <div className="main-container">
        {/* Side Menu */}
        <aside className="side-menu">
          <div className="menu-logo">
            <img src={logo} alt="My Health Tracker Logo" className="logo" />
            <h2>My Health Tracker</h2>
          </div>
          <nav>
            <ul>
              <li><i className="fas fa-home"></i> Dashboard</li>
              <li><i className="fas fa-heart"></i> Health Data</li>
              <li><i className="fas fa-chart-line"></i> Comparisons</li>
              <li><i className="fas fa-exclamation-triangle"></i> Risk Predictions</li>
              <li><i className="fas fa-cog"></i> Settings</li>
            </ul>
          </nav>
        </aside>
  
        {/* Main Content */}
        <div className="content">
          {/* Navbar */}
          <header className="navbar">
            <h1 className="welcome-text">Welcome, User!</h1>
            <button className="profile-button">
              <i className="fas fa-user-circle"></i>
            </button>
          </header>
  
          {/* Reminders Circle and Popup */}
          <button className="reminder-circle" onClick={handleRemindersClick}>
            <i className="fas fa-bell"></i>
            <span className="notification-count">3</span>
          </button>
          {showReminders && (
            <div className="reminders-popup">
              <h2>Reminders</h2>
              <ul>
                <li>Take your medication at 8:00 AM</li>
                <li>Schedule your annual health check-up</li>
                <li>Drink water and stay hydrated</li>
              </ul>
            </div>
          )}
  
          {/* Dashboard Content */}
          <section className="dashboard">
            <div className="overview-card shadow">
              <h2>Health Overview</h2>
              <p>View your recent health data trends.</p>
              <button className="btn btn-primary">View Details</button>
            </div>
  
            <div className="action-cards">
              <div className="card shadow">
                <h3>Track Health Data</h3>
                <p>Log and manage your health records efficiently.</p>
                <button className="btn btn-secondary">Track Now</button>
              </div>
              <div className="card shadow">
                <h3>Compare Data</h3>
                <p>Analyze and compare your health stats.</p>
                <button className="btn btn-secondary">Compare</button>
              </div>
              <div className="card shadow">
                <h3>Predict Risks</h3>
                <p>Get insights into potential health risks.</p>
                <button className="btn btn-secondary">Predict Risks</button>
              </div>
            </div>
          </section>
        </div>
      </div>
    );
  }

export default MainPage;
