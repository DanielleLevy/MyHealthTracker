import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
import joblib
import matplotlib.pyplot as plt

# Step 1: Load and preprocess the dataset
stroke_data = pd.read_csv("../data/healthcare-dataset-stroke-data.csv")

# Map categorical features
mapping = {
    "gender": {"Male": 1, "Female": 2, "Other": 3},
    "ever_married": {"No": 1, "Yes": 2},
    "smoking_status": {"never smoked": 1, "formerly smoked": 2, "smokes": 3, "Unknown": 0},
}
for column, map_dict in mapping.items():
    if column in stroke_data.columns:
        stroke_data[column] = stroke_data[column].map(map_dict)

# Handle missing values
stroke_data["bmi"] = stroke_data["bmi"].fillna(stroke_data["bmi"].mean())

# Drop irrelevant columns
stroke_data = stroke_data.drop(columns=["id", "Residence_type", "heart_disease", "work_type"], errors="ignore")

# Select relevant features
features = ["gender", "age", "hypertension", "ever_married", "avg_glucose_level", "bmi", "smoking_status"]
X = stroke_data[features]
y = stroke_data["stroke"]

# Scale features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

# Handle class imbalance using SMOTE
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# Train and evaluate models
models = {
    "Random Forest": RandomForestClassifier(random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    "XGBoost": XGBClassifier(random_state=42, use_label_encoder=False, eval_metric="logloss"),
}

results = {}
for model_name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred)
    results[model_name] = auc
    print(f"\nModel: {model_name}")
    print("Confusion Matrix:\n", confusion_matrix(y_test, model.predict(X_test)))
    print("Classification Report:\n", classification_report(y_test, model.predict(X_test)))

# Neural Network
print("\nEvaluating Neural Network:")
nn_model = Sequential([
    Input(shape=(X_train.shape[1],)),
    Dense(128, activation="relu"),
    Dense(64, activation="relu"),
    Dense(1, activation="sigmoid"),
])
nn_model.compile(optimizer=Adam(learning_rate=0.001), loss="binary_crossentropy", metrics=["AUC"])
nn_model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1)
nn_y_pred = nn_model.predict(X_test).flatten()
nn_auc = roc_auc_score(y_test, nn_y_pred)
results["Neural Network"] = nn_auc

# Convert NN predictions to binary
nn_y_pred_classes = (nn_y_pred > 0.5).astype(int)
print("Confusion Matrix:\n", confusion_matrix(y_test, nn_y_pred_classes))
print("Classification Report:\n", classification_report(y_test, nn_y_pred_classes))

# Save the best model
best_model_name = max(results, key=results.get)
if best_model_name == "Neural Network":
    nn_model.save("best_stroke_model.h5")
else:
    best_model = models[best_model_name]
    joblib.dump(best_model, f"best_stroke_model_{best_model_name}.pkl")

# Plot results
plt.bar(results.keys(), results.values(), color="skyblue")
plt.title("Model Performance (AUC)")
plt.ylabel("AUC Score")
plt.xlabel("Model")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("model_performance_plot_stroke.png")
plt.show()

# Save evaluation results
with open("model_evaluation_results.txt", "w") as f:
    for model_name, auc in results.items():
        f.write(f"Model: {model_name}\n")
        f.write(f"AUC: {auc:.4f}\n")
        if model_name != "Neural Network":
            conf_matrix = confusion_matrix(y_test, models[model_name].predict(X_test))
            class_report = classification_report(y_test, models[model_name].predict(X_test))
        else:
            conf_matrix = confusion_matrix(y_test, nn_y_pred_classes)
            class_report = classification_report(y_test, nn_y_pred_classes)
        f.write("Confusion Matrix:\n")
        f.write(str(conf_matrix) + "\n")
        f.write("Classification Report:\n")
        f.write(class_report + "\n")
        f.write("\n")
