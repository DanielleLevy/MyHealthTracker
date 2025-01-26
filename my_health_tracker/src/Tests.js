import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import jsPDF from "jspdf";
import "jspdf-autotable";
import * as XLSX from "xlsx";
import "./Tests.css"; // Custom styling

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
import annotationPlugin from "chartjs-plugin-annotation";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  annotationPlugin
);

const Tests = ({ tests, testList, limitsMap}) => {
  console.log("Received tests:", tests);
  console.log("Received testList:", testList);


  const exportDataAsPDF = () => {
    const doc = new jsPDF();
    doc.text("Health Checkup Report", 14, 10);
    doc.autoTable({
      head: [["Test Name", "Value", "Date"]],
      body: tests.map((test) => [
        test.test_name,
        test.value,
        new Date(test.test_date).toLocaleDateString(),
      ]),
    });
    doc.save("Health_Checkup_Report.pdf");
  };

  const exportDataAsExcel = () => {
    const data = tests.map((test) => ({
      "Test Name": test.test_name,
      Value: test.value,
      Date: new Date(test.test_date).toLocaleDateString(),
    }));

    const worksheet = XLSX.utils.json_to_sheet(data);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Tests");
    XLSX.writeFile(workbook, "Health_Checkup_Report.xlsx");
  };

  return (
    <div className="tests-container">
      <h1>Tests Overview</h1>
      <div className="export-buttons">
        <button className="export-btn" onClick={exportDataAsPDF}>
          Export as PDF
        </button>
        <button className="export-btn" onClick={exportDataAsExcel}>
          Export as Excel
        </button>
      </div>
      {[...new Set(tests.map((test) => test.test_name))].map((testName) => {
        const testData = tests
          .filter((test) => test.test_name === testName)
          .sort((a, b) => new Date(a.test_date) - new Date(b.test_date));

        const testInfo = testList.find((test) => test.test_name === testName);
        const limits = limitsMap[testName] || {};

        const graphData = {
          labels: testData.map((test) =>
            new Date(test.test_date).toLocaleDateString()
          ),
          datasets: [
            {
              label: testName,
              data: testData.map((test) => Number(test.value)),
              borderColor: "rgba(75,192,192,1)",
              borderWidth: 2,
              tension: 0.3,
              pointBackgroundColor: testData.map((test) =>
                Number(test.value) > (limits.upper_limit || Infinity) ||
                Number(test.value) < (limits.lower_limit || -Infinity)
                  ? "red"
                  : "green"
              ),
              fill: false,
            },
          ],
        };

       const graphOptions = {
  responsive: true,
  plugins: {
    annotation: {
      annotations: {
        lowerLimit: limits.lower_limit
          ? {
              type: "line",
              yMin: limits.lower_limit,
              yMax: limits.lower_limit,
              borderColor: "blue",
              borderWidth: 1,
              borderDash: [5, 5],
              label: {
                content: "Min",
                enabled: true,
                position: "start",
              },
            }
          : null,
        upperLimit: limits.upper_limit
          ? {
              type: "line",
              yMin: limits.upper_limit,
              yMax: limits.upper_limit,
              borderColor: "red",
              borderWidth: 1,
              borderDash: [5, 5],
              label: {
                content: "Max",
                enabled: true,
                position: "start",
              },
            }
          : null,
      },
    },
    legend: {
      display: true,
      position: "top",
      labels: {
        generateLabels: (chart) => {
          const datasetLabels = chart.data.datasets.map((dataset) => ({
            text: dataset.label,
            fillStyle: dataset.borderColor,
          }));

          const limitLabels = [];
          if (limits.lower_limit) {
            limitLabels.push({
              text: "Min Limit",
              fillStyle: "blue",
            });
          }
          if (limits.upper_limit) {
            limitLabels.push({
              text: "Max Limit",
              fillStyle: "red",
            });
          }

          return [...datasetLabels, ...limitLabels];
        },
      },
    },
  },
};

        return (
          <div key={testName} className="test-section">
            <h3>{testInfo?.full_name || testName}</h3>
            <p>{testInfo?.description || "No description available."}</p>
            <Line data={graphData} options={graphOptions} />
            <p>
              <strong>Most Recent Value:</strong>{" "}
              {testData[testData.length - 1].value}
            </p>
          </div>
        );
      })}
    </div>
  );
};

export default Tests;
