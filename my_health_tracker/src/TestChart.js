import React from "react";
import { Chart as ChartJS, LinearScale, PointElement, LineElement, Tooltip, Annotation } from "chart.js";
import { Scatter } from "react-chartjs-2";
import annotationPlugin from "chartjs-plugin-annotation";

// Register necessary components
ChartJS.register(LinearScale, PointElement, LineElement, Tooltip, annotationPlugin);

const TestChart = ({ test }) => {
  const { test_name, latest_value, min_range, max_range, last_test_date, is_out_of_range, is_overdue } = test;

  // Extend range dynamically based on limits and user value
  const rangeBuffer = 0.2; // Extra padding
  const rangeMin = Math.min(latest_value, min_range !== null ? min_range : latest_value) - 
                   Math.abs(latest_value * rangeBuffer);
  const rangeMax = Math.max(latest_value, max_range !== null ? max_range : latest_value) + 
                   Math.abs(latest_value * rangeBuffer);

  // Define dataset (horizontal line + user marker)
  const data = {
    datasets: [
      {
        label: test_name,
        data: [
          { x: rangeMin, y: 0 }, // Start of range
          { x: rangeMax, y: 0 }, // End of range
        ],
        borderColor: "black",
        borderWidth: 3,
        pointRadius: 0, // No points on the line
      },
      {
        label: "Your Value",
        data: [{ x: latest_value, y: 0 }], // User's test result
        backgroundColor: is_out_of_range ? "red" : "green",
        borderColor: "black",
        borderWidth: 2,
        pointRadius: 10, // Larger point
        pointHoverRadius: 12, // Hover effect
      },
    ],
  };

  // Define chart options
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        min: rangeMin,
        max: rangeMax,
        ticks: {
          stepSize: (rangeMax - rangeMin) / 5, // Dynamic step size
          callback: function(value) {
            // Only show ticks within the limits, hide others
            if ((min_range !== null && value < min_range) || (max_range !== null && value > max_range)) {
              return "";
            }
            return value.toFixed(1); // Show only relevant ticks
          }
        },
      },
      y: { display: false }, // Hide Y-axis
    },
    plugins: {
      tooltip: { enabled: true },
      annotation: {
        annotations: {
          lowerLimit: min_range !== null
            ? {
                type: "line",
                xMin: min_range,
                xMax: min_range,
                borderColor: "black",
                borderWidth: 2,
                label: {
                  display: true,
                  content: min_range.toFixed(1),
                  enabled: true,
                  position: "bottom",
                  backgroundColor: " #f9f9f9",
                  color: "black",
                  font: { size: 12, weight: "bold" },
                  yAdjust: -10, // Moves the label below the line
                },
              }
            : null,
          upperLimit: max_range !== null
            ? {
                type: "line",
                xMin: max_range,
                xMax: max_range,
                borderColor: "black",
                borderWidth: 2,
                label: {
                  display: true,
                  content: max_range.toFixed(2),
                  enabled: true,
                  position: "bottom",
                  backgroundColor: " #f9f9f9",
                  color: "black",
                  font: { size: 12, weight: "bold" },
                  yAdjust: -10, // Moves the label below the line
                },
              }
            : null,
        },
      },
    },
  };

  return (
    <div className="test-chart-container">
      <h3 className="test-title">{test_name}</h3>
      <div className="chart-area">
        <Scatter data={data} options={options} />
      </div>
      <p className="test-date">Last test: {last_test_date}</p>
      <div className="alerts">
        {is_out_of_range && <span className="alert">⚠ Out of range!</span>}
        {is_overdue && <span className="reminder">⏳ It's time for a follow-up test.</span>}
      </div>
    </div>
  );
};

export default TestChart;
