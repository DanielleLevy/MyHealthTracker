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

const ComparisonAnalysis = ({ userData, limitsMap, setActiveTab }) => {
  const [comparisonData, setComparisonData] = useState(null);
  const [testList, setTestList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch the list of tests with their names and descriptions
  useEffect(() => {
    const fetchTestList = async () => {
      try {
        const response = await axios.get("http://localhost:5001/api/get_tests");
        setTestList(response.data.tests);
      } catch (error) {
        console.error("Failed to fetch test list:", error);
      }
    };

    fetchTestList();
  }, []);

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

  const getTestInfo = (testName) => {
    const test = testList.find((t) => t.test_name === testName);
    return {
      fullName: test?.full_name || testName,
      description: test?.description || "No description available.",
    };
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
          const { fullName, description } = getTestInfo(testName);
          const userValue = comparisonData.user_tests[testName] || null;
          const bins = histogramData.map((entry) => entry.bin);
          const frequencies = histogramData.map((entry) => entry.frequency);
          const mode = bins[frequencies.indexOf(Math.max(...frequencies))];

          const calculatePercentile = (userValue, bins, frequencies) => {
            const totalUsers = frequencies.reduce((a, b) => a + b, 0);
            let cumulativeSum = 0;

            for (let i = 0; i < bins.length; i++) {
              cumulativeSum += frequencies[i];
              if (userValue < bins[i]) {
                return (cumulativeSum / totalUsers) * 100;
              }
            }
            return 100; // User value is above all bins
          };

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
              <h3>{fullName}</h3>
              <p>{description}</p>
              <Line
                data={{
                  labels: bins,
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
                      data: bins.map((_, idx) => (idx === bins.indexOf(userValue) ? frequencies[idx] : null)),
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
              <p style={{ color: "red" }}>Your Value: {userValue?.toFixed(1)}</p>
              <p style={{ fontWeight: "bold" }}>{conclusion}</p>
            </div>
          );
        })}
    </div>
  );
};

export default ComparisonAnalysis;
