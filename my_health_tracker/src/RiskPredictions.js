import React, { useState, useEffect } from "react";
import axios from "axios";
import "./RiskPredictions.css";
import LifestyleQuestionnaire from "./LifestyleQuestionnaire";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHeart, faBrain, faSyringe, faSmile } from "@fortawesome/free-solid-svg-icons";
import GaugeChart from "react-gauge-chart";

function RiskPredictions({ username, setActiveTab}) {
  const [riskModels] = useState([
    {
      name: "Heart Disease",
      endpoint: "/api/predict_heart_disease",
      description: "Check how your heart health is doing.",
      lowAdvice: "Great job! Keep up with your balanced diet, regular exercise, and stress management. Stay on top of your annual check-ups!",
      mediumAdvice: "You're doing well, but there's room for improvement. Try to incorporate more whole foods, manage your stress levels, and keep an eye on your cholesterol and blood pressure.",
      highAdvice: "It's time to take action! Consider a full heart check-up, cut down on processed foods, and make exercise a daily habit. Your heart will thank you!",
      link: "https://www.heart.org/en/healthy-living",
      icon: faHeart,
    },
    {
      name: "Stroke",
      endpoint: "/api/predict_stroke",
      description: "Find out if you're at risk for a stroke.",
      lowAdvice: "You're on the right track! Keep an active lifestyle, stay hydrated, and maintain a nutritious diet with lots of fruits and vegetables.",
      mediumAdvice: "You're doing okay, but some small changes could make a big difference. Try reducing your salt intake and keeping an eye on your blood pressure.",
      highAdvice: "This is serious—it's important to consult a doctor. Consider lifestyle changes like quitting smoking, reducing alcohol intake, and staying physically active.",
      link: "https://www.stroke.org/en/about-stroke/stroke-symptoms",
      icon: faBrain,
    },
    {
      name: "Diabetes",
      endpoint: "/api/predict_diabetes",
      description: "See where you stand with your blood sugar levels.",
      lowAdvice: "Awesome work! Keep eating a healthy, balanced diet and staying active. Regular check-ups will help you stay in control!",
      mediumAdvice: "You're at a moderate risk, so it's a good idea to cut back on refined sugars, stay active, and monitor your blood sugar levels.",
      highAdvice: "Your risk is high—taking action now is key. Consult a doctor, adopt a low-glycemic diet, and establish a solid exercise routine to manage your risk.",
      link: "https://www.diabetes.org/diabetes",
      icon: faSyringe,
    },
    {
      name: "Depression",
      endpoint: "/api/predict_depression",
      description: "Check in on your mental well-being.",
      lowAdvice: "You're in a good place! Keep engaging in activities that make you happy, stay social, and make self-care a priority.",
      mediumAdvice: "You're doing okay, but it might help to talk to someone. Try relaxation techniques like meditation, journaling, or therapy.",
      highAdvice: "You're not alone—there are people who care and want to help. Reach out to a trusted friend, family member, or mental health professional.",
      link: "https://www.nimh.nih.gov/health/topics/depression",
      icon: faSmile,
    },
  ]);
  const [results, setResults] = useState({});
  const [lifestyleData, setLifestyleData] = useState(null);

  useEffect(() => {
    axios
      .get(`http://localhost:5001/api/user_data`, { params: { username } })
      .then((response) => {
        if (response.data && response.data.smoking !== null) {
          setLifestyleData(response.data);
        }
      })
      .catch((error) => console.error("Error fetching lifestyle data:", error));
  }, [username]);

  const handlePrediction = (model) => {
    axios
      .get(`http://localhost:5001${model.endpoint}`, { params: { username } })
      .then((response) => {
        if (response.data) {
          const { probability } = response.data;
          let riskLevel = "Low";
          let advice = model.lowAdvice;
          let color = "#00ff00";
          
          if (probability >= 50 && probability < 80) {
            riskLevel = "Medium";
            advice = model.mediumAdvice;
            color = "#ff9900";
          } else if (probability >= 80) {
            riskLevel = "High";
            advice = model.highAdvice;
            color = "#ff0000";
          }

          setResults((prev) => ({
            ...prev,
            [model.name]: { riskLevel, probability, advice, color },
          }));
        }
      })
      .catch((error) => {
        console.error(`Error predicting ${model.name} Risk:`, error);
      });
  };

  return (
    <div className="risk-container">
      <h2>Health Risk Predictions</h2>
      <p className="disclaimer">These predictions are based on machine learning models and should be used for informational purposes only. Consult a healthcare professional for personalized advice.</p>
      {!lifestyleData ? (
        <div className="no-data-message">
          <p>You need to complete the lifestyle questionnaire before getting predictions.</p>
          <button className="btn btn-primary" onClick={() => setActiveTab("lifeStyle")}>Fill Questionnaire</button>
        </div>
      ) : (
        <div className="risk-results">
          {riskModels.map((model, index) => (
            <div key={index} className="risk-item">
              <div className="risk-header">
                <FontAwesomeIcon icon={model.icon} className="risk-icon" />
                <h3>{model.name} Risk</h3>
              </div>
              <p>{model.description}</p>
              <button className="btn btn-primary" onClick={() => handlePrediction(model)}>
                Predict
              </button>
              {results[model.name] && (
                <div className="gauge-chart-container">
                  <GaugeChart
                    id={`gauge-${index}`}
                    nrOfLevels={20}
                    colors={["#00ff00", "#ffcc00", "#ff0000"]}
                    arcWidth={0.3}
                    percent={results[model.name].probability / 100}
                    textColor="#000"
                    style={{ width: "400px", height: "150px" }}
                  />
                  <p style={{ color: results[model.name].color, fontWeight: "bold" }}>
                    You are at {results[model.name].riskLevel} risk for {model.name.toLowerCase()}.
                  </p>
                  <p><strong>Advice:</strong> {results[model.name].advice}</p>
                  <a href={model.link} target="_blank" rel="noopener noreferrer">Learn more</a>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default RiskPredictions;
