# frontend/dashboard.py

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import requests
import random
import json

# Initialize the Dash app with Dark theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Secure Network Topology Dashboard"

# Backend API endpoint
BACKEND_URL = "http://127.0.0.1:5000"   # Flask/FastAPI backend running

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Secure Network Topology Dashboard", className="text-center mb-4"), width=12)
    ]),

    dbc.Row([
        # Left control panel
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Controls"),
                dbc.CardBody([
                    dbc.Button("Add Random PC", id="add-pc", color="primary", className="mb-2", n_clicks=0, block=True),
                    dbc.Button("Add Random Laptop", id="add-laptop", color="info", className="mb-2", n_clicks=0, block=True),
                    dbc.Button("Add Random Server", id="add-server", color="success", className="mb-2", n_clicks=0, block=True),
                    dbc.Button("Add Random IoT Device", id="add-iot", color="warning", className="mb-2", n_clicks=0, block=True),
                    dbc.Button("Refresh Topology", id="refresh-btn", color="secondary", className="mb-2", n_clicks=0, block=True),
                ])
            ], className="mb-4"),

            dbc.Card([
                dbc.CardHeader("Network Stats"),
                dbc.CardBody([
                    html.P("Total Devices: ", id="device-count"),
                    html.P("Total Connections: ", id="edge-count"),
                    html.P("Risk Breakdown:", className="mt-3"),
                    dcc.Graph(id="risk-pie", style={"height": "250px"})
                ])
            ])
        ], width=3),

        # Right network graph panel
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Live Network Topology"),
                dbc.CardBody([
                    dcc.Graph(id="topology-graph", style={"height": "600px"})
                ])
            ])
        ], width=9),
    ]),

    dcc.Interval(id="auto-refresh", interval=5000, n_intervals=0)  # auto-refresh every 5 sec
], fluid=True)


# ---------------- CALLBACKS ----------------

@app.callback(
    Output("topology-graph", "figure"),
    Output("device-count", "children"),
    Output("edge-count", "children"),
    Output("risk-pie", "figure"),
    Input("refresh-btn", "n_clicks"),
    Input("auto-refresh", "n_intervals"),
    Input("add-pc", "n_clicks"),
    Input("add-laptop", "n_clicks"),
    Input("add-server", "n_clicks"),
    Input("add-iot", "n_clicks"),
)
def update_topology(refresh, auto, add_pc, add_laptop, add_server, add_iot):
    ctx = dash.callback_context

    # Handle button clicks → call backend to add device
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "add-pc":
            requests.post(f"{BACKEND_URL}/add_device", json={
                "name": f"PC{random.randint(10,99)}",
                "IP": f"192.168.1.{random.randint(50,150)}",
                "MAC": f"AA:BB:CC:{random.randint(10,99)}",
                "type": "PC",
                "OS": random.choice(["Windows", "Linux"]),
                "firewall": True
            })

        elif button_id == "add-laptop":
            requests.post(f"{BACKEND_URL}/add_device", json={
                "name": f"Laptop{random.randint(10,99)}",
                "IP": f"192.168.1.{random.randint(150,200)}",
                "MAC": f"AA:BB:CC:{random.randint(10,99)}",
                "type": "Laptop",
                "OS": random.choice(["Windows", "Linux"]),
                "firewall": True
            })

        elif button_id == "add-server":
            requests.post(f"{BACKEND_URL}/add_device", json={
                "name": f"Server{random.randint(10,99)}",
                "IP": f"192.168.1.{random.randint(200,250)}",
                "MAC": f"AA:BB:CC:{random.randint(10,99)}",
                "type": "Server",
                "OS": "Linux",
                "firewall": True
            })

        elif button_id == "add-iot":
            requests.post(f"{BACKEND_URL}/add_device", json={
                "name": f"IoT{random.randint(10,99)}",
                "IP": f"192.168.1.{random.randint(100,250)}",
                "MAC": f"AA:BB:CC:{random.randint(10,99)}",
                "type": "IoT",
                "OS": "RTOS",
                "firewall": random.choice([True, False])
            })

    # Fetch latest topology from backend
    response = requests.get(f"{BACKEND_URL}/topology")
    data = response.json()

    nodes = data["nodes"]
    edges = data["edges"]

    # Graph figure
    import plotly.graph_objects as go

    edge_x, edge_y = [], []
    for edge in edges:
        src, dst = edge["source"], edge["target"]
        src_node = next(n for n in nodes if n["id"] == src)
        dst_node = next(n for n in nodes if n["id"] == dst)
        edge_x += [random.random()*10, random.random()*10, None]
        edge_y += [random.random()*10, random.random()*10, None]

    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=1, color="white"), hoverinfo="none")

    node_x, node_y, text, colors = [], [], [], []
    color_map = {"PC": "blue", "Laptop": "cyan", "Server": "green", "Router": "orange", "Switch": "purple", "IoT": "red"}

    for node in nodes:
        node_x.append(random.random()*10)
        node_y.append(random.random()*10)
        text.append(f"{node['name']} ({node['type']})<br>IP: {node['IP']}<br>Risk: {node['risk_label']}")
        colors.append(color_map.get(node["type"], "grey"))

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text", text=[n["name"] for n in nodes],
        marker=dict(size=18, color=colors, line_width=2),
        textposition="bottom center", hovertext=text, hoverinfo="text"
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(showlegend=False, hovermode="closest", margin=dict(b=0,l=0,r=0,t=0),
                      paper_bgcolor="black", plot_bgcolor="black")

    # Device stats
    device_count = f"Total Devices: {len(nodes)}"
    edge_count = f"Total Connections: {len(edges)}"

    # Risk pie chart
    risk_levels = [n["risk_label"] for n in nodes]
    risk_fig = go.Figure(data=[go.Pie(labels=risk_levels, hole=0.4)])
    risk_fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor="black", font=dict(color="white"))

    return fig, device_count, edge_count, risk_fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
