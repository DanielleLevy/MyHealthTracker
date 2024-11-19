import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Define nodes (datasets)
datasets = {
    "Health Checkup Result": ["IDV_ID", "AGE_GROUP", "SEX", "BMI", "BP_HIGH", "BP_LWST", "BLDS", "TOT_CHOLE", "SMK_STAT"],
    "Heart Disease": ["age", "sex", "chol", "trestbps", "target"],
    "Depression": ["Age", "Sex", "Smoking Status", "DepressionScore"],
    "Diabetes": ["BMI", "HighBP", "HighChol", "Smoker", "Diabetes_012"],
    "Stroke": ["age", "gender", "bmi", "avg_glucose_level", "smoking_status"]
}

# Add nodes to the graph
for dataset, columns in datasets.items():
    G.add_node(dataset, label="\n".join(columns))

# Define relationships (edges)
relationships = [
    ("Health Checkup Result", "Heart Disease", "AGE_GROUP ↔ age\nSEX ↔ sex\nTOT_CHOLE ↔ chol"),
    ("Health Checkup Result", "Depression", "AGE_GROUP ↔ Age\nSEX ↔ Sex\nSMK_STAT ↔ Smoking Status"),
    ("Health Checkup Result", "Diabetes", "BMI ↔ BMI\nBP_HIGH ↔ HighBP\nSMK_STAT ↔ Smoker"),
    ("Health Checkup Result", "Stroke", "AGE_GROUP ↔ age\nSEX ↔ gender\nBMI ↔ bmi\nBLDS ↔ avg_glucose_level")
]

# Add edges with labels
for src, dst, label in relationships:
    G.add_edge(src, dst, label=label)

# Draw the graph
pos = nx.spring_layout(G)
plt.figure(figsize=(12, 8))

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='lightblue')

# Draw edges
nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20)

# Draw labels
node_labels = {node: f"{node}\n---\n{'\n'.join(datasets[node])}" for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)

# Draw edge labels
edge_labels = {(src, dst): label for src, dst, label in relationships}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

# Show the plot
plt.title("Entity-Relationship Diagram", fontsize=16)
plt.axis("off")
plt.show()
