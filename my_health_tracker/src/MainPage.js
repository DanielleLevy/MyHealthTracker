import React, { useState } from "react";
import "./MainPage.css";
import logo from './loginPage/welcome/logo.png';

function MainPage() {
  const [showReminders, setShowReminders] = useState(false);
  const [showAddTestModal, setShowAddTestModal] = useState(false);
  const [formData, setFormData] = useState({
    testName: "",
    date: "",
    value: "",
  });

  const testList = ["Blood Pressure", "Glucose Level", "Cholesterol", "Heart Rate"];

  const handleRemindersClick = () => {
    setShowReminders(!showReminders);
  };

  const handleAddTestClick = () => {
    setShowAddTestModal(true);
  };

  const handleCloseAddTestModal = () => {
    setShowAddTestModal(false);
    setFormData({ testName: "", date: "", value: "" }); // Reset form
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    alert(`Test Added:\nTest Name: ${formData.testName}\nDate: ${formData.date}\nValue: ${formData.value}`);
    handleCloseAddTestModal();
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
          <button className="reminder-btn" onClick={handleRemindersClick}>
            <i className="fas fa-bell"></i>
          </button>
          {showReminders && (
            <div className="reminders-popover">
              <h2>Reminders</h2>
              <ul>
                <li>Take your medication at 8:00 AM</li>
                <li>Schedule your annual health check-up</li>
                <li>Drink water and stay hydrated</li>
              </ul>
            </div>
          )}
        </header>

        {/* Add New Test Button */}
        <button className="add-test-btn" onClick={handleAddTestClick}>
          <i className="fas fa-plus"></i>
        </button>

        {/* Add Test Modal */}
        {showAddTestModal && (
          <div className="modal-overlay">
            <div className="modal-content">
              <h2>Add Test</h2>
              <form onSubmit={handleFormSubmit}>
                <label>
                  Test Name:
                  <select name="testName" value={formData.testName} onChange={handleInputChange} required>
                    <option value="">Select Test</option>
                    {testList.map((test, index) => (
                      <option key={index} value={test}>{test}</option>
                    ))}
                  </select>
                </label>
                <label>
                  Date:
                  <input
                    type="date"
                    name="date"
                    value={formData.date}
                    onChange={handleInputChange}
                    required
                  />
                </label>
                <label>
                  Value:
                  <input
                    type="text"
                    name="value"
                    value={formData.value}
                    onChange={handleInputChange}
                    placeholder="Enter Value"
                    required
                  />
                </label>
                <div className="modal-actions">
                  <button type="submit" className="btn btn-primary">Add Test</button>
                  <button type="button" className="btn btn-secondary" onClick={handleCloseAddTestModal}>Cancel</button>
                </div>
              </form>
            </div>
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
