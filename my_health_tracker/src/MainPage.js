import React, { useState, useEffect } from "react";
import axios from "axios";
import "./MainPage.css";
import logo from './loginPage/welcome/logo.png';
import Tests from "./Tests"; 
import ComparisonAnalysis from "./ComparisonAnalysis";
import TestChart from "./TestChart"; 
import PersonalInformation from "./PersonalInformation";
import LifestyleQuestionnaire from "./LifestyleQuestionnaire";
import RiskPredictions from "./RiskPredictions";


function MainPage() {
  const [username, setUsername] = useState(localStorage.getItem("username") || "User");
  const [showReminders, setShowReminders] = useState(false);
  const [showAddTestModal, setShowAddTestModal] = useState(false);
  const [activeTab, setActiveTab] = useState("dashboard");
  const [healthAlerts, setHealthAlerts] = useState([]);
  const [testList, setTestList] = useState([]); // שמירת רשימת הבדיקות
  const [userData, setUserData] = useState(null);

  const renderTabContent = () => {
  switch (activeTab) {
    case "dashboard":
      return (
        <div>
          <h2 className="title-sum">Health Summary</h2>
          <p>Let's take a look at your most recent test results!</p>
          <section className="dashboard">
            <div className="overview-card shadow">
              {userData?.testSummary?.length > 0 ? (
                userData.testSummary.map((test, index) => <TestChart key={index} test={test} />)
              ) : (
                <p>No recent tests available.</p>
              )}
            </div>
          </section>
        </div>
      );
    
case "tests":
    return (
        <Tests
            tests={userData?.tests || []}
            testList={testList}
            fetchTestLimits={fetchTestLimits} // מעביר את הפונקציה כ-prop
        />
    );

   case "riskPredictions":
        return <RiskPredictions username={username} />;

    case "lifeStyle":
      return <LifestyleQuestionnaire username={username} />;
    case "comparisonAnalysis":
      return <ComparisonAnalysis userData={userData} />;
    case "PersonalInformation":
      return <PersonalInformation userData={userData} setUserData={setUserData} />;      
    default:
      return <div>404 - Page not found</div>;
  }
};

  const [formData, setFormData] = useState({
    testName: "",
    date: "",
    value: "",
  });

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
          fetchHealthAlerts(username); 
          fetchHealthSummary(username);
        }
      })
      .catch((error) => {
        console.error("Error fetching user data:", error);
      });
  axios.get('http://localhost:5001/api/get_tests')
    .then((response) => {
      if (response.data && response.data.tests) {
        console.log("Tests fetched:", response.data.tests);
        setTestList(response.data.tests || []); // עדכון testList
      }
    })
    .catch((error) => {
      console.error("Error fetching test list:", error);
    });
}, [username]);
const fetchTestLimits = async (testName) => {
    try {
        const response = await axios.get('http://localhost:5001/api/get_test_limits', {
            params: { username, test_name: testName }
        });
        console.log(`Limits for ${testName}:`, response.data);
        return response.data; // נחזיר את נתוני המינימום והמקסימום
    } catch (error) {
        console.error(`Error fetching limits for ${testName}:`, error);
        return null;
    }
};

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


  const fetchHealthAlerts = (username) => {
    axios.get("http://localhost:5001/api/user_health_alerts", { params: { username } })
      .then(response => {
        if (response.data && response.data.alerts) {
          setHealthAlerts(response.data.alerts);
        }
      })
      .catch(error => console.error("Error fetching health alerts:", error));
  };
  
  const fetchHealthSummary = (username) => {
    axios.get("http://localhost:5001/api/user_test_summary", { params: { username } })
    .then(response => {
      if (response.data) {
        setUserData(prevData => ({ ...prevData, testSummary: response.data.tests }));
      }
    })
    .catch(error => console.error("Error fetching test summary:", error));
  };
  
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
          console.log("Tests fetched:", response.data.tests); // הדפסת המידע
          setTestList(response.data.tests || []); // עדכון רשימת הבדיקות עם שם הבדיקה המלא
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
                    <i className="fas fa-home"></i> Health Summary
                </li>
                <li className={activeTab === "tests" ? "active" : ""} onClick={() => setActiveTab("tests")}>
                    <i className="fas fa-vial"></i> Tests
                </li>
                <li
                    className={activeTab === "riskPredictions" ? "active" : ""}
                    onClick={() => setActiveTab("riskPredictions")}
                >
                    <i className="fas fa-exclamation-triangle"></i> Risk Predictions
                </li>
                <li className={activeTab === "comparisonAnalysis" ? "active" : ""}
                    onClick={() => setActiveTab("comparisonAnalysis")}>
                    <i className="fas fa-chart-bar"></i> Comparison Analysis
                </li>
                <li className={activeTab === "lifeStyle" ? "active" : ""} onClick={() => setActiveTab("lifeStyle")}>
                    <i className="fas fa-brain"></i> Life Style
                </li>
                <li className={activeTab === "PersonalInformation" ? "active" : ""}
                    onClick={() => setActiveTab("PersonalInformation")}>
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
                         {test.full_name}
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

export default MainPage;