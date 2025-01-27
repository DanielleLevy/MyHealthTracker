import React, { useEffect, useState } from "react";
import axios from "axios";
import LifestyleQuestionnaire from "./LifestyleQuestionnaire";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";

// Registering Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

// 📌 שמות ותיאורי בדיקות
const testNameMap = {
  HMG: "Hemoglobin",
  BP_HIGH: "Systolic Blood Pressure",
  BP_LWST: "Diastolic Blood Pressure",
  TOT_CHOLE: "Total Cholesterol",
  TRIGLYCERIDE: "Triglycerides",
};

const testDescriptionMap = {
  HMG: "Measures hemoglobin levels, important for oxygen transport in the blood.",
  BP_HIGH: "Indicates systolic blood pressure, measuring the pressure in arteries during heartbeats.",
  BP_LWST: "Indicates diastolic blood pressure, measuring the pressure in arteries between heartbeats.",
  TOT_CHOLE: "Measures total cholesterol levels in the blood.",
  TRIGLYCERIDE: "Indicates triglyceride levels, a type of fat found in the blood.",
};

// bin size calculation
const calculateBinSize = (values, method = "sturges") => {
  const N = values.length;
  if (N < 2) return 5; // ברירת מחדל במקרה של מעט נתונים

  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);
  const range = maxValue - minValue;

  // חישוב IQR
  const sortedValues = [...values].sort((a, b) => a - b);
  const q1 = sortedValues[Math.floor(0.25 * N)];
  const q3 = sortedValues[Math.floor(0.75 * N)];
  const IQR = q3 - q1;

  // Freedman-Diaconis לחישוב bin width
  let binWidth = 2 * (IQR / Math.cbrt(N));

  // 📌 הגבלת גודל בין (Bin Width) לטווח הגיוני
  binWidth = Math.min(Math.max(binWidth, 2), 10); // בין 2 ל-10

  return binWidth;
};



const ComparisonAnalysis = ({ userData, limitsMap, setActiveTab }) => {
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (userData) {
      const { username, smoking, drinking, physical_activity, education_levels, age_group } = userData;

      if (!username || smoking === undefined || drinking === undefined || physical_activity === undefined || education_levels === undefined || age_group === undefined) {
        setError("Missing lifestyle data. Please complete your profile.");
        return;
      }

      fetchComparisonData(username, smoking, drinking, physical_activity, education_levels, age_group);
    }
  }, [userData]);

  const fetchComparisonData = async (username, smoking, drinking, physical_activity, education_levels, age_group) => {
    try {
      setLoading(true);
      setError(null);

      const response = await axios.get("http://localhost:5001/api/compare_tests", {
        params: { username, smoking, drinking, physical_activity, education_levels, age_group },
      });

      console.log("API response:", response.data);
      setComparisonData(response.data);
    } catch (err) {
      console.error("Error fetching comparison data:", err);
      setError("Failed to fetch comparison data.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: "100vh" }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="no-data-message">
        <p>You need to complete the lifestyle questionnaire before getting comparisons.</p>
        <button className="btn btn-primary" onClick={() => setActiveTab("lifeStyle")}>Fill Questionnaire</button>
    </div>
    );
  }

  return (
    <div>
      <h2>Comparison Analysis</h2>
      <p>Here you can compare your latest test results with users who have a similar lifestyle.</p>

      {comparisonData &&
        Object.entries(comparisonData.histograms).map(([testName, histogramData], index) => {
          const userValue = comparisonData.user_tests[testName] || null;
          const values = histogramData.map((entry) => entry.bin);
          const binSize = calculateBinSize(values);

          const bins = histogramData.map((entry) => entry.bin);
          const frequencies = histogramData.map((entry) => entry.frequency);
          const userBinIndex = bins.findIndex((bin) => userValue >= bin && userValue < bin + binSize);

          const calculatePercentile = (userValue, bins, frequencies) => {
            const totalUsers = frequencies.reduce((a, b) => a + b, 0);
            let cumulativeSum = 0;
          
            for (let i = 0; i < bins.length; i++) {
              cumulativeSum += frequencies[i];
              if (userValue < bins[i]) {
                return (cumulativeSum / totalUsers) * 100;
              }
            }
            return 100; // אם המשתמש מעל כולם
          };
          
          const mode = bins[frequencies.indexOf(Math.max(...frequencies))]; // ערך השיא בהתפלגות
          const medianIndex = Math.floor(frequencies.length / 2);
          const median = bins[medianIndex]; // חציון ההתפלגות
          
          const userPercentile = calculatePercentile(userValue, bins, frequencies);
          
          const conclusion =
            userPercentile < 10
              ? "Your result is significantly lower than most users in your group."
              : userPercentile > 90
              ? "Your result is significantly higher than most users in your group."
              : userValue < mode
              ? "Your result is below the most common range among similar users."
              : userValue > mode
              ? "Your result is above the most common range among similar users."
              : "Your result falls within the typical range of similar users.";
          

          return (
            <div key={index} style={{ marginBottom: "40px" }}>
              <h3>{testNameMap[testName] || testName}</h3>
              <p>{testDescriptionMap[testName] || "No description available."}</p>
              <Line
                data={{
                  labels: bins.map((bin, index, arr) => 
                    index < arr.length - 1 ? `${bin.toFixed(1)} - ${(arr[index + 1] - 0.01).toFixed(1)}` : `${bin.toFixed(1)}+`
                ),
                  datasets: [
                    {
                      label: "Population Distribution",
                      data: frequencies,
                      backgroundColor: "rgba(75, 192, 192, 0.4)",
                      borderColor: "rgba(75, 192, 192, 1)",
                      borderWidth: 1,
                      fill: true,
                    },
                    {
                      label: "Your Value",
                      data: bins.map((_, idx) => (idx === userBinIndex ? frequencies[idx] : null)),
                      backgroundColor: "rgba(255, 99, 132, 1)",
                      borderColor: "rgba(255, 99, 132, 1)",
                      borderWidth: 3,
                      pointRadius: 6,
                      pointBackgroundColor: "rgba(255, 99, 132, 1)",
                    },
                  ],
                }}
                options={{
                  responsive: true,
                  plugins: {
                    legend: { position: "top" },
                    tooltip: {
                      callbacks: {
                        label: function (tooltipItem) {
                          return `Value: ${tooltipItem.raw}`;
                        },
                      },
                    },
                  },
                  scales: {
                    x: { title: { display: true, text: "Test Value Ranges" } },
                    y: { title: { display: true, text: "Number of People" }, beginAtZero: true },
                  },
                }}
              />
              <p style={{ color: "red" }}>Your Value: {userValue.toFixed(1)}</p>
              <p style={{ fontWeight: "bold" }}>{conclusion}</p>
            </div>
          );
        })}
    </div>
  );
};

export default ComparisonAnalysis;
