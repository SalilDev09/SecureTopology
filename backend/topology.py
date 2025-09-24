import networkx as nx
import pandas as pd
from ml_model.risk_model import predict_security


def create_topology():
    """
    Create a sample network topology with security predictions
    using the ML model.
    """

    G = nx.Graph()

    # 🔹 Devices with improved dummy features
    #    (replace with real dataset values later)
    devices = [
        ("PC1", "PC", {"firewall": 1, "vulnerabilities": 3, "bandwidth": 50, "latency": 10}),
        ("PC2", "PC", {"firewall": 0, "vulnerabilities": 5, "bandwidth": 40, "latency": 20}),
        ("Laptop1", "Laptop", {"firewall": 1, "vulnerabilities": 2, "bandwidth": 60, "latency": 15}),
        ("Laptop2", "Laptop", {"firewall": 1, "vulnerabilities": 4, "bandwidth": 55, "latency": 18}),
        ("Server1", "Server", {"firewall": 1, "vulnerabilities": 1, "bandwidth": 100, "latency": 5}),
        ("Server2", "Server", {"firewall": 0, "vulnerabilities": 6, "bandwidth": 80, "latency": 25}),
        ("Router1", "Router", {"firewall": 1, "vulnerabilities": 2, "bandwidth": 90, "latency": 8}),
        ("Switch1", "Switch", {"firewall": 1, "vulnerabilities": 3, "bandwidth": 70, "latency": 12}),
        ("IoT1", "IoT", {"firewall": 0, "vulnerabilities": 7, "bandwidth": 20, "latency": 30}),
        ("IoT2", "IoT", {"firewall": 0, "vulnerabilities": 8, "bandwidth": 15, "latency": 35}),
    ]

    # Convert features to DataFrame for ML model
    features_df = pd.DataFrame([d[2] for d in devices])
    security_labels = predict_security(features_df)  # 0 = insecure, 1 = secure, or risk score

    # Function: classify risk based on vulnerabilities
    def classify_risk(vulns: int) -> str:
        if vulns <= 2:
            return "Low"
        elif 3 <= vulns <= 5:
            return "Medium"
        else:
            return "High"

    # Add nodes with ML-predicted secure flag + risk levels
    for i, (device_name, device_type, feats) in enumerate(devices):
        risk_level = classify_risk(feats["vulnerabilities"])
        G.add_node(
            device_name,
            type=device_type,
            secure=int(security_labels[i]),
            risk=risk_level,
            **feats
        )

    # Define network connections
    edges = [
        ("PC1", "Switch1"), ("PC2", "Switch1"),
        ("Laptop1", "Switch1"), ("Laptop2", "Switch1"),
        ("Server1", "Switch1"), ("Server2", "Switch1"),
        ("Switch1", "Router1"),
        ("Router1", "IoT1"), ("Router1", "IoT2"),
    ]

    # Add edges with security depending on connected nodes
    for u, v in edges:
        G.add_edge(u, v, secure=int(G.nodes[u]["secure"] and G.nodes[v]["secure"]))

    return G


# 🔹 Alias for backward compatibility
def generate_topology():
    return create_topology()
