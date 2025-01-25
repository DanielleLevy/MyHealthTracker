import React, { useState } from "react";
import axios from "axios";
import "./RiskPredictions.css";

function RiskPredictions({ username }) {
  const [riskModels] = useState([
    {
      name: "Heart Disease Risk",
      endpoint: "/api/predict_heart_disease",
      description: "Assess your risk of heart disease.",
      advice: "Consider reducing stress, avoiding smoking, and scheduling an appointment with a cardiologist for regular check-ups.",
      link: "https://www.heart.org/en/healthy-living"
    },
    {
      name: "Stroke Risk",
      endpoint: "/api/predict_stroke",
      description: "Assess your risk of stroke.",
      advice: "Pay attention to symptoms such as sudden weakness, confusion, or difficulty speaking. Seek immediate medical attention if needed.",
      link: "https://www.stroke.org/en/about-stroke/stroke-symptoms"
    },
    {
      name: "Diabetes Risk",
      endpoint: "/api/predict_diabetes",
      description: "Assess your risk of diabetes.",
      advice: "Maintain a healthy diet, exercise regularly, and monitor blood sugar levels. Consider consulting an endocrinologist.",
      link: "https://www.diabetes.org/diabetes"
    },
    {
      name: "Depression Risk",
      endpoint: "/api/predict_depression",
      description: "Assess your risk of depression.",
      advice: "If you're feeling down for an extended period, reach out to a mental health professional. Self-care and a support system can help.",
      link: "https://www.nimh.nih.gov/health/topics/depression"
    },
  ]);
  const [results, setResults] = useState({});

  const handlePrediction = (model) => {
    axios
      .get(`http://localhost:5001${model.endpoint}`, { params: { username } })
      .then((response) => {
        if (response.data) {
          const { risk_level, probability } = response.data;
          setResults((prev) => ({
            ...prev,
            [model.name]: { risk_level, probability },
          }));
        } else {
          console.error(`Empty response for ${model.name}`);
          alert(`Prediction for ${model.name} returned an empty response.`);
        }
      })
      .catch((error) => {
        console.error(`Error predicting ${model.name}:`, error);
        if (error.response && error.response.data.error) {
          alert(`Failed to get ${model.name} prediction: ${error.response.data.error}`);
        } else {
          alert(`Failed to get ${model.name} prediction. Please check your server.`);
        }
      });
  };

  return (
    <div className="content">
      <h2>Risk Predictions</h2>
      <p>
        Please note: The following predictions are based on machine learning models
        and are for informational purposes only. Consult your doctor for professional advice.
      </p>
      <div className="action-cards">
        {riskModels.map((model, index) => (
          <div key={index} className="card">
            <div className="card-icon">
              <i className="fas fa-heartbeat"></i>
            </div>
            <h3>{model.name}</h3>
            <p>{model.description}</p>
            <button className="btn btn-primary" onClick={() => handlePrediction(model)}>
              Predict
            </button>
            {results[model.name] && (
              <div className="prediction-result">
                <div className="result-box">
                  <h4>Results</h4>
                  <p>
                    <strong>Risk Level:</strong> {results[model.name].risk_level}
                  </p>
                  <p>
                    <strong>Probability:</strong> {results[model.name].probability}%
                  </p>
                  <p>
                    <strong>Advice:</strong> {model.advice}
                  </p>
                  <p>
                    <a href={model.link} target="_blank" rel="noopener noreferrer">
                      Learn more
                    </a>
                  </p>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default RiskPredictions;
