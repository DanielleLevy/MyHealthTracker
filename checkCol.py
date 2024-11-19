import kagglehub
import pandas as pd
import os

# Define Kaggle dataset IDs
datasets = {
    "Health Checkup Result": "hongseoi/health-checkup-result",
    "Heart Disease": "johnsmith88/heart-disease-dataset",
    "Depression": "anthonytherrien/depression-dataset",
    "Diabetes": "alexteboul/diabetes-health-indicators-dataset",
    "Stroke": "fedesoriano/stroke-prediction-dataset"
}

# Download datasets and check columns
for dataset_name, dataset_id in datasets.items():
    try:
        # Download dataset
        path = kagglehub.dataset_download(dataset_id)
        print(f"Dataset '{dataset_name}' downloaded to: {path}")

        # Find CSV file in the downloaded directory
        csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
        if csv_files:
            # Load the first CSV file in the directory
            file_path = os.path.join(path, csv_files[0])
            df = pd.read_csv(file_path)
            # Print dataset information
            print(f"Dataset: {dataset_name}")
            print(f"Columns: {list(df.columns)}\n")
        else:
            print(f"No CSV files found in {path} for dataset '{dataset_name}'.\n")
    except Exception as e:
        print(f"Error downloading or loading {dataset_name}: {e}")
