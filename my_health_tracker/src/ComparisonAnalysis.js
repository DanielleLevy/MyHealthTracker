import React, { useEffect, useState } from "react";
import axios from "axios";

const ComparisonAnalysis = ({ userData }) => {
  const [comparisonData, setComparisonData] = useState(null);

  // Fetch comparison data function
  const fetchComparisonData = async (smoking, drinking, physical_activity, education_levels) => {
    try {
      const response = await axios.get("http://localhost:5001/api/compare_tests", {
        params: { smoking, drinking, physical_activity, education_levels },
      });
      console.log("Comparison data received:", response.data);
      setComparisonData(response.data);
    } catch (error) {
      console.error("Error fetching comparison data:", error);
    }
  };

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

  if (!comparisonData) {
    return <p>Loading comparison data...</p>;
  }

  return (
    <div>
      <h2>Test Results Comparison</h2>
      <ul>
        {comparisonData.map((item, index) => (
          <li key={index}>
            <strong>{item.test_name}:</strong> Your value: {item.your_value},
            Average: {item.avg_value.toFixed(2)},
            Standard Deviation: {item.std_dev_value.toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ComparisonAnalysis;
