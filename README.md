# 🩺 MyHealthTracker

MyHealthTracker is a full-stack health monitoring web application that allows users to track medical test results, assess risk for chronic conditions, and visualize personal health trends. It leverages machine learning models to provide personalized health risk predictions based on lifestyle, demographic, and test data.

Developed by: Danielle Hodaya Shrem & Shiran Levi  
Year: 2025

---

## 📑 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Usage](#usage)
- [Machine Learning Models](#machine-learning-models)
- [API Overview](#api-overview)
- [Test Accounts](#test-accounts)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## ✨ Features

- User sign-up, login, and profile management
- Medical test entry and history tracking
- Personalized health risk predictions:
  - Heart disease
  - Stroke
  - Diabetes
  - Depression
- Comparison to similar users using lifestyle filters
- Test alerts and health notifications
- Lifestyle questionnaire for improved predictions
- Export test data to PDF or Excel

---

## 📁 Project Structure

```
MyHealthTracker/
├── backend/               # Flask backend with APIs and DB access
├── models/                # Machine learning models and training scripts
├── my_health_tracker/     # React frontend
├── run_servers.sh         # Linux startup script
├── run_servers.bat        # Windows startup script
├── requirements.txt       # Python dependencies
├── Software Documentation.pdf
├── User_Manual___My_Health_Tracker.pdf
```

---

## 🛠️ Technologies Used

### Backend
- Python 3.x
- Flask
- MySQL
- SQLAlchemy
- Pandas

### Frontend
- React.js
- JavaScript
- Bootstrap
- CSS

### ML Models
- Scikit-learn
- XGBoost
- Gradient Boosting
- Neural Networks

---

## 🚀 Installation

### Prerequisites

- Python 3.x
- Node.js v16+
- MySQL Server
- Git Bash (recommended for Windows)

### Clone the repository

```bash
git clone https://github.com/DanielleLevy/MyHealthTracker.git
cd MyHealthTracker
```

### Backend setup

```bash
pip install -r requirements.txt
```

### Frontend setup

```bash
cd my_health_tracker
npm install
cd ..
```

---

## ▶️ Running the App

From the root folder:

- **Windows**:  
  ```bash
  ./run_servers.bat
  ```

- **Linux/Mac**:  
  ```bash
  ./run_servers.sh
  ```

App will run at: [http://localhost:3000](http://localhost:3000)

---

## 🧑‍💻 Usage

### 1. Sign Up / Login

- Users must provide username, password, date of birth, gender, height, and weight.
- BMI is calculated automatically.

### 2. Dashboard

- Shows latest test results and alerts for abnormal values.
- Visual indicators and history graphs per test.

### 3. Add Test Results

- Add from any page via the ➕ button.
- Only one test per type per date is allowed.

### 4. Lifestyle Questionnaire

- Must be completed to unlock prediction and comparison features.

### 5. Risk Predictions

- Navigate to "Risk Predictions"
- Click on a disease category and select **Predict**
- Displays risk level (Low, Medium, High) and guidance

### 6. Compare with Similar Users

- Histogram view showing where your test stands relative to others with similar age/lifestyle.

---

## 🤖 Machine Learning Models

All models are pre-trained and stored in the `/models/` folder.

| Condition     | Model Used         | Input Features |
|---------------|--------------------|----------------|
| Heart Disease | Gradient Boosting  | BP, Cholesterol, Glucose, Age, Gender |
| Stroke        | XGBoost            | BP, Glucose, BMI, Lifestyle |
| Diabetes      | XGBoost            | BP, BMI, Cholesterol, Lifestyle |
| Depression    | Neural Network     | Lifestyle + Demographic |

Predictions are made via Flask API endpoints, integrated with real-time user data.

---

## 🌐 API Overview

Located in: `backend/auth_api.py`

### User Management
- `POST /api/signup`  
- `POST /api/login`  
- `GET /api/user_data`

### Health Data
- `POST /api/add_test`
- `GET /api/get_user_tests`
- `GET /api/get_tests`
- `GET /api/user_health_alerts`
- `GET /api/user_test_summary`

### Lifestyle
- `GET /api/get_lifestyle_info`
- `POST /api/update_lifestyle_info`

### ML Predictions
- `GET /api/predict_heart_disease`
- `GET /api/predict_stroke`
- `GET /api/predict_diabetes`
- `GET /api/predict_depression`

---

## 🧪 Test Accounts

To login with a test account:

- **Username**: any number from `1` to `500000`  
- **Password**: `pass` + username  

✅ These accounts are preloaded with real medical test data.

---

## 🧯 Troubleshooting

### Port already in use?
- Make sure ports `3000` (frontend) and `5001` (backend) are free.

### Windows issues?
- Use **Git Bash** instead of Command Prompt to run shell scripts.

### Logs not showing?
- Check terminal output after script execution.

---

## 📝 License

© 2025 My Health Tracker. All rights reserved.  
This project is for educational and informational use only.  
Health predictions are not medical advice. Always consult a licensed professional.

---
