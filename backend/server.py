from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# in-memory topology
topology = {
    "nodes": [],
    "edges": []
}

@app.route("/topology", methods=["GET"])
def get_topology():
    return jsonify(topology)

@app.route("/add_device", methods=["POST"])
def add_device():
    data = request.json
    node_id = len(topology["nodes"]) + 1
    node = {
        "id": node_id,
        "name": data.get("name"),
        "IP": data.get("IP"),
        "MAC": data.get("MAC"),
        "type": data.get("type"),
        "OS": data.get("OS"),
        "firewall": data.get("firewall"),
        "risk_label": random.choice(["Low", "Medium", "High"])
    }
    topology["nodes"].append(node)
    # optional: connect to some random existing nodes
    if topology["nodes"] and len(topology["nodes"]) > 1:
        other = random.choice([n["id"] for n in topology["nodes"] if n["id"] != node_id])
        topology["edges"].append({"source": node_id, "target": other})
    return jsonify(node), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)
