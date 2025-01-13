import React from "react";
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
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const testNameMap = {
  "BLDS": "Pre-meal Blood Glucose",
  "BP_HIGH": "Systolic Blood Pressure",
  "BP_LWST": "Diastolic Blood Pressure",
  "TOT_CHOLE": "Total Cholesterol",
  "TRIGLYCERIDE": "Triglycerides",
  "HDL_CHOLE": "HDL Cholesterol",
  "LDL_CHOLE": "LDL Cholesterol",
  "CREATININE": "Serum Creatinine",
  "HMG": "Hemoglobin",
  "OLIG_PROTE_CD": "Urinary Protein Excretion",
  "SGOT_AST": "AST (Liver Function)",
  "SGPT_ALT": "ALT (Liver Function)",
  "GAMMA_GTP": "Gamma GTP (Liver Function)"
};

const testDescriptionMap = {
  "BLDS": "Measures blood glucose levels before a meal.",
  "BP_HIGH": "Indicates systolic blood pressure, measuring the pressure in arteries during heartbeats.",
  "BP_LWST": "Indicates diastolic blood pressure, measuring the pressure in arteries between heartbeats.",
  "TOT_CHOLE": "Measures total cholesterol levels in the blood.",
  "TRIGLYCERIDE": "Indicates triglyceride levels, a type of fat found in the blood.",
  "HDL_CHOLE": "Measures 'good' HDL cholesterol, which helps remove other forms of cholesterol.",
  "LDL_CHOLE": "Measures 'bad' LDL cholesterol, which can build up in arteries.",
  "CREATININE": "Indicates kidney function by measuring creatinine levels in the blood.",
  "HMG": "Measures hemoglobin levels, important for oxygen transport in the blood.",
  "OLIG_PROTE_CD": "Indicates protein excretion in urine, a sign of kidney health.",
  "SGOT_AST": "Measures AST enzyme levels, indicating liver function.",
  "SGPT_ALT": "Measures ALT enzyme levels, another marker of liver function.",
  "GAMMA_GTP": "Measures GGT enzyme levels, related to liver and bile duct function."
};

const Tests = ({ tests }) => {
  console.log("Received tests:", tests);

  // Handle case with no tests
  if (!tests || tests.length === 0) {
    return <p>No test data available. Please add tests.</p>;
  }

  // Get unique test names
  const uniqueTestNames = [...new Set(tests.map((test) => test.test_name))];
  const exportDataAsPDF = () => {
    const doc = new jsPDF();
    doc.text("Health Checkup Report", 14, 10);
    doc.autoTable({
      head: [["Test Name", "Value", "Date"]],
      body: tests.map((test) => [
        testNameMap[test.test_name] || test.test_name,
        test.value,
        new Date(test.test_date).toLocaleDateString(),
      ]),
    });
    doc.save("Health_Checkup_Report.pdf");
  };

  const exportDataAsExcel = () => {
    const data = tests.map((test) => ({
      "Test Name": testNameMap[test.test_name] || test.test_name,
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
          <button className="export-btn" onClick={() => exportDataAsPDF()}>
            Export as PDF
          </button>
          <button className="export-btn" onClick={() => exportDataAsExcel()}>
            Export as Excel
          </button>
        </div>
        {uniqueTestNames.map((testName) => {
          const testData = tests.filter((test) => test.test_name === testName);
          const graphData = {
            labels: testData.map((test) =>
                new Date(test.test_date).toLocaleDateString()
            ),
            datasets: [
              {
                label: testNameMap[testName] || testName,
                data: testData.map((test) => Number(test.value)),
                borderColor: "rgba(75,192,192,1)",
                borderWidth: 2,
                tension: 0.3,
                pointBackgroundColor: testData.map((test) =>
                    Number(test.value) > 150 || Number(test.value) < 50
                        ? "red"
                        : "green"
                ),
                fill: false,
              },
            ],
          };

          return (
              <div key={testName} className="test-section">
                <h3>{testNameMap[testName] || testName}</h3>
                <p>{testDescriptionMap[testName]}</p>
                <Line data={graphData} options={{responsive: true}}/>
                <p>
                  <strong>Most Recent Value:</strong> {testData[testData.length - 1].value}
                </p>
              </div>
          );
        })}
      </div>
  );
};

export default Tests;
