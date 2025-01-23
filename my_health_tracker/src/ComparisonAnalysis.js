import React, { useEffect, useState } from "react";
import axios from "axios";
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

// Map for test names and descriptions
const testNameMap = {
  BLDS: "Pre-meal Blood Glucose",
  BP_HIGH: "Systolic Blood Pressure",
  BP_LWST: "Diastolic Blood Pressure",
  TOT_CHOLE: "Total Cholesterol",
  TRIGLYCERIDE: "Triglycerides",
  HDL_CHOLE: "HDL Cholesterol",
  LDL_CHOLE: "LDL Cholesterol",
  CREATININE: "Serum Creatinine",
  HMG: "Hemoglobin",
  OLIG_PROTE_CD: "Urinary Protein Excretion",
  SGOT_AST: "AST (Liver Function)",
  SGPT_ALT: "ALT (Liver Function)",
  GAMMA_GTP: "Gamma GTP (Liver Function)",
};

const testDescriptionMap = {
  BLDS: "Measures blood glucose levels before a meal.",
  BP_HIGH: "Indicates systolic blood pressure, measuring the pressure in arteries during heartbeats.",
  BP_LWST: "Indicates diastolic blood pressure, measuring the pressure in arteries between heartbeats.",
  TOT_CHOLE: "Measures total cholesterol levels in the blood.",
  TRIGLYCERIDE: "Indicates triglyceride levels, a type of fat found in the blood.",
  HDL_CHOLE: "Measures 'good' HDL cholesterol, which helps remove other forms of cholesterol.",
  LDL_CHOLE: "Measures 'bad' LDL cholesterol, which can build up in arteries.",
  CREATININE: "Indicates kidney function by measuring creatinine levels in the blood.",
  HMG: "Measures hemoglobin levels, important for oxygen transport in the blood.",
  OLIG_PROTE_CD: "Indicates protein excretion in urine, a sign of kidney health.",
  SGOT_AST: "Measures AST enzyme levels, indicating liver function.",
  SGPT_ALT: "Measures ALT enzyme levels, another marker of liver function.",
  GAMMA_GTP: "Measures GGT enzyme levels, related to liver and bile duct function.",
};

const ComparisonAnalysis = ({ userData }) => {
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (userData) {
      const { smoking, drinking, physical_activity, education_levels, age_group } = userData;

      if (
        smoking !== undefined &&
        drinking !== undefined &&
        physical_activity !== undefined &&
        education_levels !== undefined &&
        age_group !== undefined
      ) {
        fetchComparisonData(smoking, drinking, physical_activity, education_levels, age_group);
      } else {
        setError("Incomplete user data.");
        console.error("Incomplete user data:", userData);
      }
    }
  }, [userData]);

  const fetchComparisonData = async (smoking, drinking, physical_activity, education_levels, age_group) => {
    try {
      setLoading(true);
      setError(null);

      const response = await axios.get("http://localhost:5001/api/compare_tests", {
        params: {
          smoking,
          drinking,
          physical_activity,
          education_levels,
          age_group,
        },
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
    return <p>Loading comparison data...</p>;
  }

  if (error) {
    return <p style={{ color: "red" }}>Error: {error}</p>;
  }

  return (
    <div>
      {comparisonData.map((test, index) => {
        console.log("Rendering Test:", test);

        if (!test.histogram) {
          console.warn(`Histogram is missing for test: ${test.test_name}`);
          return (
            <div key={index}>
              <h3>{testNameMap[test.test_name] || test.test_name}</h3>
              <p>No data available for this test (Missing histogram).</p>
            </div>
          );
        }

        if (!Array.isArray(test.histogram)) {
          try {
            test.histogram = JSON.parse(test.histogram);
            console.log(`Parsed histogram for test: ${test.test_name}`, test.histogram);
          } catch (e) {
            console.error(`Failed to parse histogram for test: ${test.test_name}`, test.histogram);
            return (
              <div key={index}>
                <h3>{testNameMap[test.test_name] || test.test_name}</h3>
                <p>No data available for this test (Histogram not an array).</p>
              </div>
            );
          }
        }

        if (test.histogram.every(val => val === 0)) {
          console.warn(`All histogram values are zero for test: ${test.test_name}`);
          return (
            <div key={index}>
              <h3>{testNameMap[test.test_name] || test.test_name}</h3>
              <p>No data available for this test (All values are zero).</p>
            </div>
          );
        }

     const binSize = test.bin_size || 1;
        const labels = test.histogram.map((_, idx) => `${(idx * 10).toFixed(1)}-${((idx + 1) * 10).toFixed(1)}`);

        const maxLabels = 20;
        const step = Math.ceil(labels.length / maxLabels);
        const reducedLabels = labels.filter((_, idx) => idx % step === 0);
        const reducedHistogram = test.histogram.filter((_, idx) => idx % step === 0);
        const chartData = reducedHistogram.map((value, index) => ({
          x: index * 10, // ערך X: אינדקס כפול גודל בין (למשל, 0, 10, 20, ...)
          y: value,      // ערך Y: ספירת ההיסטוגרמה
        }));
        if (reducedLabels.length !== reducedHistogram.length) {
          console.error(
            `Mismatch: Reduced Labels (${reducedLabels.length}) and Reduced Histogram (${reducedHistogram.length}) lengths do not match for test: ${test.test_name}`
          );
          return (
            <div key={index}>
              <h3>{testNameMap[test.test_name] || test.test_name}</h3>
              <p style={{ color: "red" }}>Error: Mismatch in reduced data lengths for this test.</p>
            </div>
          );
        }

        const userValueIndex = Math.floor(test.your_value / binSize);
        const userValue = userValueIndex < test.histogram.length ? test.histogram[userValueIndex] : null;

        if (userValue === null) {
          console.warn(`User value (${test.your_value}) does not match any bin.`);
        }

        return (
          <div key={index} style={{ marginBottom: "40px" }}>
            <h3>{testNameMap[test.test_name] || test.test_name}</h3>
            <p>{testDescriptionMap[test.test_name] || "No description available."}</p>
            <Line
              data={{
                datasets: [
                  {
                    label: "Population Distribution",
                    data: chartData, // שימוש במערך הנקודות החדש
                    backgroundColor: "rgba(75, 192, 192, 0.4)",
                    borderColor: "rgba(75, 192, 192, 1)",
                    borderWidth: 1,
                    fill: true,
                  },
                  {
                    label: "Your Value",
                    data: [{ x: Math.floor(test.your_value / 10) * 10, y: 0 }], // נקודה בודדת
                    pointStyle: 'rectRot',
                    backgroundColor: "rgba(255, 99, 132, 1)",
                    borderColor: "rgba(255, 99, 132, 1)",
                    borderWidth: 3,
                    pointRadius: 8,
                    pointBackgroundColor: "rgba(255, 99, 132, 1)",
                    pointRotation: 45,
                  },
                ],
              }}
              options={{
                responsive: true,
                plugins: {
                  legend: {
                    position: "top",
                  },
                  tooltip: {
                    callbacks: {
                      label: function (tooltipItem) {
                        return `Value: ${tooltipItem.raw}`;
                      },
                    },
                  },
                },
                 scales: {
                  x: {
                    type: 'linear', // חשוב: הגדרת סוג סקאלה לינארית
                    title: {
                      display: true,
                      text: "Value Range", // שינוי הטקסט
                    },
                    ticks: {
                      stepSize: 10
                    }
                  },
                  y: {
                    title: {
                      display: true,
                      text: "Frequency",
                    },
                    beginAtZero: true,
                  },
                },
              }}
            />
            <p style={{ color: "red" }}>Your Value: {test.your_value}</p>
          </div>
        );
      })}
    </div>
  );
};

export default ComparisonAnalysis;
