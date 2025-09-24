# backend/devices.py

import networkx as nx
import random

class DeviceManager:
    def __init__(self):
        self.graph = nx.Graph()
        self.device_counter = 0

        # Preload initial devices
        initial_devices = [
            {"name": "PC1", "IP": "192.168.1.1", "MAC": "AA:BB:CC:01", "type": "PC", "OS": "Windows", "firewall": True},
            {"name": "PC2", "IP": "192.168.1.2", "MAC": "AA:BB:CC:02", "type": "PC", "OS": "Linux", "firewall": True},
            {"name": "Laptop1", "IP": "192.168.1.3", "MAC": "AA:BB:CC:03", "type": "Laptop", "OS": "Windows", "firewall": True},
            {"name": "Laptop2", "IP": "192.168.1.4", "MAC": "AA:BB:CC:04", "type": "Laptop", "OS": "Linux", "firewall": True},
            {"name": "Server1", "IP": "192.168.1.10", "MAC": "AA:BB:CC:10", "type": "Server", "OS": "Linux", "firewall": True},
            {"name": "Server2", "IP": "192.168.1.11", "MAC": "AA:BB:CC:11", "type": "Server", "OS": "Linux", "firewall": True},
            {"name": "Router1", "IP": "192.168.1.254", "MAC": "AA:BB:CC:FF", "type": "Router", "OS": "Linux", "firewall": True},
            {"name": "Switch1", "IP": "192.168.1.100", "MAC": "AA:BB:CC:AA", "type": "Switch", "OS": "Firmware", "firewall": True},
            {"name": "IoT1", "IP": "192.168.1.200", "MAC": "AA:BB:CC:BB", "type": "IoT", "OS": "RTOS", "firewall": False},
            {"name": "IoT2", "IP": "192.168.1.201", "MAC": "AA:BB:CC:CC", "type": "IoT", "OS": "RTOS", "firewall": False}
        ]

        for d in initial_devices:
            self.add_device(**d)

    def add_device(self, name, IP, MAC, type, OS, firewall):
        """
        Add a new device dynamically into the graph.
        Judges will see it pop up in the live network map.
        """
        self.device_counter += 1

        # Simple security risk logic
        if firewall and type != "IoT":
            risk_label = "Secure"
            risk_level = "Low"
        elif firewall and type == "IoT":
            risk_label = "Insecure"
            risk_level = "Medium"
        else:
            risk_label = "Insecure"
            risk_level = "High"

        device_data = {
            "id": f"dev{self.device_counter}",
            "name": name,
            "IP": IP,
            "MAC": MAC,
            "type": type,
            "OS": OS,
            "firewall": firewall,
            "risk_label": risk_label,
            "risk_level": risk_level
        }

        self.graph.add_node(device_data["id"], **device_data)

        # Randomly connect to an existing node if available
        if len(self.graph.nodes) > 1:
            existing_node = random.choice(list(self.graph.nodes))
            if existing_node != device_data["id"]:
                self.graph.add_edge(device_data["id"], existing_node)

        return device_data

    def get_topology(self):
        """Return topology data for frontend (nodes + edges)."""
        nodes = [self.graph.nodes[n] for n in self.graph.nodes]
        edges = [{"source": u, "target": v} for u, v in self.graph.edges]
        return {"nodes": nodes, "edges": edges}


# If you want to test standalone
if __name__ == "__main__":
    dm = DeviceManager()
    new_device = dm.add_device("NewIoT", "192.168.1.250", "AA:BB:CC:DD", "IoT", "RTOS", False)
    print("Added:", new_device)
    print("Topology:", dm.get_topology())
