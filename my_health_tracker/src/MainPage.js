import React, { useState, useEffect } from "react";
import axios from "axios";
import "./MainPage.css";
import logo from './loginPage/welcome/logo.png';
import Tests from "./Tests"; 
import ComparisonAnalysis from "./ComparisonAnalysis";
import PersonalInformation from "./PersonalInformation";


function MainPage() {
  const [username, setUsername] = useState(localStorage.getItem("username") || "User");
  const [showReminders, setShowReminders] = useState(false);
  const [showAddTestModal, setShowAddTestModal] = useState(false);
  const [activeTab, setActiveTab] = useState("dashboard");
  const renderTabContent = () => {
  switch (activeTab) {
    case "dashboard":
      return (
        <div>
          <h2>Dashboard</h2>

          <section className="dashboard">
            <div className="overview-card shadow">
              <h2>Health Overview</h2>
              <p>View your recent health data trends.</p>
              <button className="btn btn-primary">View Details</button>
            </div>

            <div className="action-cards">
              <div className="card shadow" onClick={() => console.log('Track Health')}>
                <i className="fas fa-heartbeat card-icon"></i>
                <h3>Track Health</h3>
              </div>
              <div className="card shadow" onClick={() => console.log('Predict Risks')}>
                <i className="fas fa-chart-line card-icon"></i>
                <h3>Predict Risks</h3>
              </div>
              <div className="card shadow" onClick={() => console.log('Mental Health')}>
                <i className="fas fa-brain card-icon"></i>
                <h3>Mental Health</h3>
              </div>
            </div>
          </section>
        </div>

      );
    case "tests":
      return <Tests tests={userData?.tests || []} />;
    case "riskPredictions":
      return <div>Risk Predictions Content</div>;
    case "mentalHealth":
      return <div>Mental Health Content</div>;
    case "comparisonAnalysis":
      return <ComparisonAnalysis userData={userData} />;
    case "PersonalInformation":
      return <PersonalInformation userData={userData} setUserData={setUserData} />;      
    default:
      return <div>404 - Page not found</div>;
  }
};

  const [userData, setUserData] = useState(null);
  const [testList, setTestList] = useState([]); // רשימת בדיקות
  const [formData, setFormData] = useState({
    testName: "",
    date: "",
    value: "",
  });

  const testNameMap = {
    "BLDS": "Pre-meal Blood Glucose",
    "BP_HIGH": "Systolic Blood Pressure",
    "BP_LWST": "Diastolic Blood Pressure",
    "TOT_CHOLE": "Total Cholesterol",
    "TRIGLYCERIDE": "Triglycerides",
    "HDL_CHOLE": "HDL Cholesterol",
    "LDL_CHOLE": "LDL Cholesterol",
    "CREATININE": "Serum Creatinine",
    "HMG": "Hemoglobin",
    "OLIG_PROTE_CD": "Urinary Protein Excretion",
    "SGOT_AST": "AST (Liver Function)",
    "SGPT_ALT": "ALT (Liver Function)",
    "GAMMA_GTP": "Gamma GTP (Liver Function)"
  };

  useEffect(() => {
    if (!username || username === "User") {
      console.error("Username not found in localStorage!");
      return;
    }

    axios.get('http://localhost:5001/api/user_data', { params: { username } })
      .then((response) => {
        if (response.data) {
          const user = response.data;
          user.BMI = calculateBMI(user.height, user.weight);
          setUserData(user);
          console.log("User Data Received:", user);

          // Fetch user tests after receiving user data
          fetchUserTests(username);
        }
      })
      .catch((error) => {
        console.error("Error fetching user data:", error);
      });
  }, [username]);

  const fetchUserTests = (username) => {
    axios.get('http://localhost:5001/api/get_user_tests', { params: { username } })
      .then((response) => {
        if (response.data && response.data.tests) {
          setUserData((prevData) => ({ ...prevData, tests: response.data.tests }));
          console.log("User Tests Received:", response.data.tests);
        }
      })
      .catch((error) => {
        console.error("Error fetching user tests:", error);
      });
  };

  const healthAlerts = userData && userData.tests ? getHealthAlerts(userData.tests) : [];

  const calculateBMI = (height, weight) => {
    if (!height || !weight) return "N/A";
    const heightInMeters = height / 100;
    return (weight / (heightInMeters * heightInMeters)).toFixed(2);
  };

  const handleAddTestClick = () => {
    setShowAddTestModal(true);

    axios.get('http://localhost:5001/api/get_tests')
      .then((response) => {
        if (response.data && response.data.tests) {
          setTestList(response.data.tests || []);
        }
      })
      .catch((error) => {
        console.error("Error fetching test list:", error);
      });
  };

  const handleCloseAddTestModal = () => {
    setShowAddTestModal(false);
    setFormData({ testName: "", date: "", value: "" });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();

    axios.post('http://localhost:5001/api/add_test', {
      username,
      test_name: formData.testName,
      test_date: formData.date,
      value: formData.value,
    })
      .then(() => {
        alert("Test added successfully!");
        handleCloseAddTestModal();
        fetchUserTests(username); // Refresh user tests after adding a new one
      })
      .catch((error) => {
        console.error("Error adding test:", error);
        alert("Failed to add test.");
      });
  };

  return (
    <div className="main-container">
      <aside className="side-menu">
        <div className="menu-logo">
          <img src={logo} alt="My Health Tracker Logo" className="logo" />
          <h2>My Health Tracker</h2>
        </div>
        <nav>
          <ul>
            <li className={activeTab === "dashboard" ? "active" : ""} onClick={() => setActiveTab("dashboard")}>
              <i className="fas fa-home"></i> Dashboard
            </li>
            <li className={activeTab === "tests" ? "active" : ""} onClick={() => setActiveTab("tests")}>
              <i className="fas fa-vial"></i> Tests
            </li>
            <li className={activeTab === "riskPredictions" ? "active" : ""} onClick={() => setActiveTab("riskPredictions")}>
              <i className="fas fa-exclamation-triangle"></i> Risk Predictions
            </li>
            <li className={activeTab === "comparisonAnalysis" ? "active" : ""} onClick={() => setActiveTab("comparisonAnalysis")}>
              <i className="fas fa-chart-bar"></i> Comparison Analysis
            </li>
            <li className={activeTab === "mentalHealth" ? "active" : ""} onClick={() => setActiveTab("mentalHealth")}>
              <i className="fas fa-brain"></i> Mental Health
            </li>
            <li className={activeTab === "PersonalInformation" ? "active" : ""} onClick={() => setActiveTab("PersonalInformation")}>
              <i className="bi bi-info-circle"></i> Personal Information
            </li>
          </ul>
        </nav>

      </aside>

      <div className="content">
        <header className="navbar">
        <h1 className="welcome-text">Welcome, {username}!</h1>
        <button className="reminder-btn" onClick={() => setShowReminders(!showReminders)}>
            <i className="fas fa-bell"></i>
            {healthAlerts.length > 0 && (
              <span className="notification-badge">{healthAlerts.length}</span>
            )}
          </button>
          {showReminders && (
            <div className="reminders-popover">
              <h2>Health Alerts</h2>
              <section className="health-alerts">
            {healthAlerts.length > 0 ? (
              <ul>
                {healthAlerts.map((alert, index) => (
                  <li key={index} style={{color: "red", fontWeight: "bold"}}>
                    <i class="bi bi-exclamation-triangle alert-icon"></i>
                    {alert}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No health alerts. You're doing great!</p>
            )}
          </section>
            </div>
          )}
        </header>
        {renderTabContent()}

        <button className="add-test-btn" onClick={handleAddTestClick}>
          <i className="fas fa-plus"></i>
        </button>

        {showAddTestModal && (
          <div className="modal-overlay">
            <div className="modal-content">
              <h2>Add Test</h2>
              <form onSubmit={handleFormSubmit}>
                <label>
                  Test Name:
                  <select
                    name="testName"
                    value={formData.testName}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="">Select Test</option>
                    {testList.map((test, index) => (
                      <option key={index} value={test}>
                        {testNameMap[test] || test}
                      </option>
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
      </div>
    </div>
  );
}

function getHealthAlerts(tests) {
  const latestTests = {};

  tests.forEach((test) => {
    if (!latestTests[test.test_name] || new Date(test.test_date) > new Date(latestTests[test.test_name].test_date)) {
      latestTests[test.test_name] = test;
    }
  });

  const alerts = [];

  Object.values(latestTests).forEach((test) => {
    if (test.test_name === "BP_HIGH" && test.value > 120) {
      alerts.push("High systolic blood pressure detected!");
    }
    if (test.test_name === "BP_LWST" && test.value > 80) {
      alerts.push("High diastolic blood pressure detected!");
    }
    if (test.test_name === "LDL_CHOLE" && test.value > 170) {
      alerts.push("High LDL Cholesterol detected!");
    }
    if (test.test_name === "HDL_CHOLE" && test.value < 30) {
      alerts.push("Low HDL Cholesterol detected!");
    }
    if (test.test_name === "TRIGLYCERIDE" && test.value > 150) {
      alerts.push("High Triglyceride levels detected!");
    }
    if (test.test_name === "CREATININE" && (test.value < 0.8 || test.value > 1.7)) {
      alerts.push("Abnormal Creatinine levels detected!");
    }
  });

  return alerts;
}

export default MainPage;