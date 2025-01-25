import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import joblib

# Step 1: Load the dataset
heart = pd.read_csv("../data/heart.csv")  # Ensure the correct path to your CSV

# Step 2: Select relevant features
features = ["age", "sex", "trestbps", "chol", "fbs"]
X = heart[features]
y = heart["target"]

# Step 3: Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Split the data into training and testing sets (80/20 split)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 5: Train and evaluate multiple models
models = {
    "Logistic Regression": LogisticRegression(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42)
}

results = {}
for model_name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred)
    results[model_name] = auc

# Step 6: Train a Neural Network
nn_model = Sequential([
    Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    Dense(32, activation="relu"),
    Dense(1, activation="sigmoid")
])
nn_model.compile(optimizer=Adam(learning_rate=0.001), loss="binary_crossentropy", metrics=["AUC"])
nn_model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)
nn_y_pred = nn_model.predict(X_test).flatten()
nn_auc = roc_auc_score(y_test, nn_y_pred)
results["Neural Network"] = nn_auc

# Step 7: Save the best model
best_model_name = max(results, key=results.get)
if best_model_name == "Neural Network":
    nn_model.save("best_heart_disease_model.h5")
else:
    best_model = models[best_model_name]
    joblib.dump(best_model, "best_heart_disease_model.pkl")

# Step 8: Create a DataFrame for results
results_df = pd.DataFrame({
    "Model": list(results.keys()),
    "AUC": list(results.values())
}).sort_values(by="AUC", ascending=False)

# Save results to CSV
results_df.to_csv("model_performance_results_heart.csv", index=False)

# Step 9: Plot the results
plt.figure(figsize=(10, 6))
plt.bar(results_df["Model"], results_df["AUC"], color="skyblue")
plt.title("Model Performance (AUC)")
plt.xlabel("Model")
plt.ylabel("AUC")
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("model_performance_plot_heart.png")
plt.show()
