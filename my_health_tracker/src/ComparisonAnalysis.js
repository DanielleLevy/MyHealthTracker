import React, { useEffect, useState } from "react";
import { Scatter } from "react-chartjs-2";
import axios from "axios";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend
);

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

  useEffect(() => {
    if (userData) {
      const { smoking, drinking, physical_activity, education_levels } = userData;

      if (
        smoking !== undefined &&
        drinking !== undefined &&
        physical_activity !== undefined &&
        education_levels !== undefined
      ) {
        fetchComparisonData(smoking, drinking, physical_activity, education_levels);
      } else {
        console.error("Incomplete user data:", userData);
      }
    }
  }, [userData]);

  const fetchComparisonData = async (smoking, drinking, physical_activity, education_levels) => {
    try {
      const response = await axios.get("http://localhost:5001/api/compare_tests", {
        params: { smoking, drinking, physical_activity, education_levels },
      });
      setComparisonData(response.data);
    } catch (error) {
      console.error("Error fetching comparison data:", error);
    }
  };

  if (!comparisonData) {
    return <p>Loading comparison data...</p>;
  }

  return (
    <div>
      <h2>Test Results Comparison</h2>
      {comparisonData.map((test, index) => (
        <div key={index} style={{ marginBottom: "40px" }}>
          <h3>{testNameMap[test.test_name] || test.test_name}</h3>
          <p>{testDescriptionMap[test.test_name]}</p>
          <Scatter
            data={{
              datasets: [
                {
                  label: "Population Distribution",
                  data: test.distribution.map((count, i) => ({
                    x: test.min_value + (i + 0.5) * ((test.max_value - test.min_value) / 10),
                    y: count,
                  })),
                  backgroundColor: "rgba(75, 192, 192, 0.6)",
                },
                {
                  label: "Your Value",
                  data: [{ x: test.your_value, y: 0 }],
                  backgroundColor: "rgba(255, 99, 132, 1)",
                  pointRadius: 8,
                },
              ],
            }}
            options={{
              scales: {
                x: {
                  title: {
                    display: true,
                    text: "Test Values",
                  },
                },
                y: {
                  title: {
                    display: true,
                    text: "Number of People",
                  },
                },
              },
            }}
          />
        </div>
      ))}
    </div>
  );
};

export default ComparisonAnalysis;