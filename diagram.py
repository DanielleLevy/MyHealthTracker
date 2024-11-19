from graphviz import Digraph

# Initialize diagram
er_diagram = Digraph(format='png', engine='dot')
er_diagram.attr(rankdir='LR', size='8,5')

# Define nodes for each dataset
datasets = {
    "Health Checkup Result": "IDV_ID\nAGE_GROUP\nSEX\nBMI\nBP_HIGH\nBP_LWST\nBLDS\nTOT_CHOLE\nSMK_STAT",
    "Heart Disease": "age\nsex\nchol\ntrestbps\ntarget",
    "Depression": "Age\nSex\nSmoking Status\nDepressionScore",
    "Diabetes": "BMI\nHighBP\nHighChol\nSmoker\nDiabetes_012",
    "Stroke": "age\ngender\nbmi\navg_glucose_level\nsmoking_status"
}

# Add dataset nodes
for dataset, columns in datasets.items():
    er_diagram.node(dataset, f"{dataset}\n---\n{columns}", shape='box', style='rounded,filled', color='lightblue')

# Define relationships (edges)
relationships = [
    ("Health Checkup Result", "Heart Disease", "AGE_GROUP ↔ age\nSEX ↔ sex\nTOT_CHOLE ↔ chol"),
    ("Health Checkup Result", "Depression", "AGE_GROUP ↔ Age\nSEX ↔ Sex\nSMK_STAT ↔ Smoking Status"),
    ("Health Checkup Result", "Diabetes", "BMI ↔ BMI\nBP_HIGH ↔ HighBP\nSMK_STAT ↔ Smoker"),
    ("Health Checkup Result", "Stroke", "AGE_GROUP ↔ age\nSEX ↔ gender\nBMI ↔ bmi\nBLDS ↔ avg_glucose_level")
]

# Add edges to diagram
for src, dst, label in relationships:
    er_diagram.edge(src, dst, label=label, fontsize='10')

# Render the diagram to a file
file_path = 'er_diagram'
er_diagram.render(file_path, format='png', cleanup=True)

print(f"ER Diagram saved as {file_path}.png")
