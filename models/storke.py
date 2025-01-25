import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import joblib

# Step 1: Load the dataset
stroke_data = pd.read_csv("../data/healthcare-dataset-stroke-data.csv")

# Step 2: Map categorical features to match your scale
mapping = {
    "gender": {"Male": 1, "Female": 2, "Other": 3},
    "ever_married": {"No": 1, "Yes": 2},  # 1 = Single, 2 = Married
    "smoking_status": {"never smoked": 1, "formerly smoked": 2, "smokes": 3, "Unknown": 0},
}

# Apply mappings
for column, map_dict in mapping.items():
    if column in stroke_data.columns:
        stroke_data[column] = stroke_data[column].map(map_dict)

# Drop irrelevant features
stroke_data = stroke_data.drop(columns=["id", "Residence_type", "heart_disease","work_type"], errors="ignore")

# Handle missing values for BMI
stroke_data["bmi"] = stroke_data["bmi"].fillna(stroke_data["bmi"].mean())

# Step 3: Select relevant features
features = [
    "gender",
    "age",
    "hypertension",
    "ever_married",
    "avg_glucose_level",
    "bmi",
    "smoking_status"
]
X = stroke_data[features]
y = stroke_data["stroke"]

# Step 4: Scale the features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Step 5: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 6: Handle class imbalance using SMOTE
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# Step 7: Train and evaluate multiple models
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
k = 3
knn_model = KNeighborsClassifier(n_neighbors=k)
knn_model.fit(X_train, y_train)
y_pred_knn = knn_model.predict(X_test)
knn_test_acc = accuracy_score(y_test, y_pred_knn)
results["KNN"] = knn_test_acc
print(f"KNN (k={k}) - Test Accuracy: {knn_test_acc}")

# Step 8: Train a Neural Network
nn_model = Sequential([
    Input(shape=(X_train.shape[1],)),
    Dense(128, activation="relu"),
    Dense(64, activation="relu"),
    Dense(32, activation="relu"),
    Dense(1, activation="sigmoid")
])
nn_model.compile(optimizer=Adam(learning_rate=0.001), loss="binary_crossentropy", metrics=["AUC"])
nn_model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1)
nn_y_pred = nn_model.predict(X_test).flatten()
nn_auc = roc_auc_score(y_test, nn_y_pred)
results["Neural Network"] = nn_auc

# Step 9: Save the best model
best_model_name = max(results, key=results.get)
if best_model_name == "Neural Network":
    nn_model.save("best_stroke_model.h5")
else:
    best_model = models[best_model_name]
    joblib.dump(best_model, f"best_stroke_model_{best_model_name}.pkl")

# Step 10: Create a DataFrame for results
results_df = pd.DataFrame({
    "Model": list(results.keys()),
    "AUC": list(results.values())
}).sort_values(by="AUC", ascending=False)

# Save results to CSV
results_df.to_csv("model_performance_results_stroke.csv", index=False)

# Step 11: Plot the results
plt.figure(figsize=(10, 6))
plt.bar(results_df["Model"], results_df["AUC"], color="skyblue")
plt.title("Model Performance (AUC)")
plt.xlabel("Model")
plt.ylabel("AUC")
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("model_performance_plot_stroke.png")
plt.show()