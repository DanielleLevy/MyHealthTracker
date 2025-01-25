import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import joblib

# Step 1: Load the dataset
depression = pd.read_csv("../data/depression_data.csv")  # Ensure the correct path to your CSV

# Step 2: Map categorical features to numerical values
mapping = {
    "Marital Status": {"Single": 1, "Married": 2, "Divorced": 3, "Widowed": 4},
    "Education Level": {
        "High School": 1,
        "Associate Degree": 2,
        "Bachelor's Degree": 3,
        "Master's Degree": 4,
        "PhD": 5,
    },
    "Physical Activity Level": {"Sedentary": 1, "Moderate": 2, "Active": 3},
    "Employment Status": {"Unemployed": 0, "Employed": 1},
    "Alcohol Consumption": {"Low": 0, "Moderate": 1, "High": 1},
    "Dietary Habits": {"Healthy": 1, "Moderate": 2, "Unhealthy": 3},
    "Sleep Patterns": {"Good": 1, "Fair": 2, "Poor": 3},
    "Smoking Status": {"Non-smoker": 1, "Former": 2, "Smoker": 3, "Current": 3},
    "History of Mental Illness": {"No": 0, "Yes": 1},
}

for column, map_dict in mapping.items():
    depression[column] = depression[column].map(map_dict)

# Step 3: Select relevant features
features = [
    "Age",
    "Marital Status",
    "Education Level",
    "Number of Children",
    "Smoking Status",
    "Physical Activity Level",
    "Employment Status",
    "Alcohol Consumption",
    "Dietary Habits",
    "Sleep Patterns",
]
X = depression[features]
y = depression["History of Mental Illness"]  # Assuming this is the target column

# Step 4: Handle missing values
X = X.copy()  # Avoid SettingWithCopyWarning
X.fillna(X.mean(), inplace=True)  # Replace NaN values with column mean

# Check for invalid data types in X before scaling
print("X dtypes before scaling:")
print(X.dtypes)

# Replace NaN or infinite values in X before scaling
X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)

# Step 5: Scale the features for Logistic Regression and KNN
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Step 6: Split the data into training and testing sets (80/20 split)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 7: Handle class imbalance using SMOTE
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# Check y_train values
print("y_train unique values after SMOTE:", np.unique(y_train, return_counts=True))

# Step 8: Train and evaluate multiple models
models = {
    "Logistic Regression": LogisticRegression(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    "XGBoost": XGBClassifier(random_state=42, use_label_encoder=False, eval_metric="logloss")
}

results = {}
for model_name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred)
    results[model_name] = auc

# Cross-validation for XGBoost with StratifiedKFold
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
xgb_auc_scores = []
for train_idx, val_idx in cv.split(X_scaled, y):
    X_train_cv, X_val_cv = X_scaled[train_idx], X_scaled[val_idx]
    y_train_cv, y_val_cv = y.iloc[train_idx], y.iloc[val_idx]

    xgb_model = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric="logloss")
    xgb_model.fit(X_train_cv, y_train_cv)
    y_pred_cv = xgb_model.predict_proba(X_val_cv)[:, 1]
    xgb_auc_scores.append(roc_auc_score(y_val_cv, y_pred_cv))

# Calculate mean AUC score
xgb_mean_auc = np.mean(xgb_auc_scores)
print("Cross-validated AUC for XGBoost:", xgb_mean_auc)
results["XGBoost (Stratified CV)"] = xgb_mean_auc

# K-Nearest Neighbors (KNN)
k = 3  # Try different values of k
knn_model = KNeighborsClassifier(n_neighbors=k)
knn_model.fit(X_train, y_train)
y_pred_knn = knn_model.predict(X_test)
knn_test_acc = accuracy_score(y_test, y_pred_knn)
results["KNN"] = knn_test_acc
print(f"KNN (k={k}) - Test Accuracy: {knn_test_acc}")

# Logistic Regression (Accuracy)
log_reg_model = LogisticRegression(random_state=42)
log_reg_model.fit(X_train, y_train)
log_reg_train_acc = log_reg_model.score(X_train, y_train)
log_reg_test_acc = accuracy_score(y_test, log_reg_model.predict(X_test))
results["Logistic Regression (Accuracy)"] = log_reg_test_acc
print(f"Logistic Regression - Train Accuracy: {log_reg_train_acc}, Test Accuracy: {log_reg_test_acc}")

# Step 9: Train a Neural Network
nn_model = Sequential([
    Input(shape=(X_train.shape[1],)),  # Updated to use Input layer
    Dense(128, activation="relu"),
    Dense(64, activation="relu"),
    Dense(32, activation="relu"),
    Dense(1, activation="sigmoid")
])
nn_model.compile(optimizer=Adam(learning_rate=0.001), loss="binary_crossentropy", metrics=["AUC"])
nn_model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)
nn_y_pred = nn_model.predict(X_test).flatten()
nn_auc = roc_auc_score(y_test, nn_y_pred)
results["Neural Network"] = nn_auc

# Step 10: Save the best model
best_model_name = max(results, key=results.get)

if best_model_name == "Neural Network":
    nn_model.save("best_depression_model.h5")
elif best_model_name in models:
    best_model = models[best_model_name]
    joblib.dump(best_model, "best_depression_model.pkl")
elif best_model_name == "KNN":
    joblib.dump(knn_model, "best_knn_model.pkl")
elif best_model_name == "Logistic Regression (Accuracy)":
    joblib.dump(log_reg_model, "best_logistic_regression_model_depression.pkl")
else:
    print(f"Unknown model name: {best_model_name}")

# Step 11: Create a DataFrame for results
results_df = pd.DataFrame({
    "Model": list(results.keys()),
    "AUC": list(results.values())
}).sort_values(by="AUC", ascending=False)

# Save results to CSV
results_df.to_csv("model_performance_results_depression.csv", index=False)

# Step 12: Plot the results
plt.figure(figsize=(10, 6))
plt.bar(results_df["Model"], results_df["AUC"], color="skyblue")
plt.title("Model Performance (AUC and Accuracy)")
plt.xlabel("Model")
plt.ylabel("Metric")
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("model_performance_plot_depression.png")
plt.show()
