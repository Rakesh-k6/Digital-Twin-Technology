"""
CityLink - Bangalore Infrastructure Graph & Topology
Models the real interconnected South Bangalore cyber-physical network:
1. Central Silk Board (Infamous junction connecting Hosur Road & Outer Ring Road, Elevated Flyover & Metro line)
2. Koramangala (Sony World Junction, 80ft Road, 100ft Road, Startup Hub)
3. HSR Layout (Sectors 1-7, 27th Main, BDA Complex, Residential & Commercial artery)
4. Bellandur (Outer Ring Road, RMZ Ecospace, Prestige Tech Park, High-density IT corridor)
"""

import networkx as nx
from typing import Dict, List, Any


def build_city_graph() -> nx.DiGraph:
    """
    Constructs the multi-layer Bengaluru Cyber-Physical Infrastructure Graph.
    Includes:
    - Road Corridors (Outer Ring Road, Hosur Road, Sarjapur Road, 80ft Road)
    - Silk Board Elevated Flyover & Namma Metro Yellow/Blue Line Viaduct
    - BESCOM (Bangalore Electricity Supply Company) 66kV/11kV Substation & Feeders
    - Critical IT Parks & Hospitals (RMZ Ecospace, St. John's Hospital, BDA Complex)
    """
    G = nx.DiGraph()

    # Bangalore Zone Metadata
    zones = {
        "Zone_A": {
            "name": "Koramangala",
            "landmark": "Sony World Junction & 80ft Road",
            "center": (-90.0, 0.0, 90.0),
            "type": "Commercial & Tech Startup Hub",
            "feeder": "BESCOM_F_KOR",
            "characteristics": "Darshini cafes, tech offices, dense pedestrian nightlife"
        },
        "Zone_B": {
            "name": "HSR_Layout",
            "landmark": "27th Main & BDA Complex",
            "center": (90.0, 0.0, 90.0),
            "type": "Planned Residential & Commercial Spine",
            "feeder": "BESCOM_F_HSR",
            "characteristics": "Tree-lined avenues, startup offices, wide footpaths"
        },
        "Zone_C": {
            "name": "Bellandur",
            "landmark": "RMZ Ecospace & Outer Ring Road (ORR)",
            "center": (90.0, 0.0, -90.0),
            "type": "Heavy IT & Technology Corridor",
            "feeder": "BESCOM_F_BEL",
            "characteristics": "Massive tech parks, heavy BMTC bus traffic, high peak EV load"
        },
        "Zone_D": {
            "name": "Silk_Board",
            "landmark": "Central Silk Board & Hosur Road Junction",
            "center": (-90.0, 0.0, -90.0),
            "type": "Critical Transit Bottleneck & Metro Interchange",
            "feeder": "BESCOM_F_SLK",
            "characteristics": "Multi-tier flyover, Namma Metro construction, highest congestion index in India"
        }
    }

    for zid, zdata in zones.items():
        G.add_node(zid, layer="zone", **zdata)

    # Bangalore Intersections
    intersections = {
        # Koramangala
        "INT_KOR_1": {"zone": "Zone_A", "name": "Sony World Junction", "pos": (-130.0, 0.0, 130.0), "has_signal": True, "feeder": "FEEDER_KOR"},
        "INT_KOR_2": {"zone": "Zone_A", "name": "80ft Road 4th Block", "pos": (-50.0, 0.0, 130.0), "has_signal": True, "feeder": "FEEDER_KOR"},
        "INT_KOR_3": {"zone": "Zone_A", "name": "Koramangala Water Tank", "pos": (-130.0, 0.0, 50.0), "has_signal": True, "feeder": "FEEDER_KOR"},
        "INT_KOR_4": {"zone": "Zone_A", "name": "St. John's Hospital Gate", "pos": (-50.0, 0.0, 50.0), "has_signal": True, "feeder": "FEEDER_KOR"},

        # HSR Layout
        "INT_HSR_1": {"zone": "Zone_B", "name": "HSR BDA Complex", "pos": (50.0, 0.0, 130.0), "has_signal": True, "feeder": "FEEDER_HSR"},
        "INT_HSR_2": {"zone": "Zone_B", "name": "27th Main Commercial Road", "pos": (130.0, 0.0, 130.0), "has_signal": True, "feeder": "FEEDER_HSR"},
        "INT_HSR_3": {"zone": "Zone_B", "name": "HSR Club Sector 2", "pos": (50.0, 0.0, 50.0), "has_signal": True, "feeder": "FEEDER_HSR"},
        "INT_HSR_4": {"zone": "Zone_B", "name": "HSR-ORR Entry Ramp", "pos": (130.0, 0.0, 50.0), "has_signal": True, "feeder": "FEEDER_HSR"},

        # Bellandur
        "INT_BEL_1": {"zone": "Zone_C", "name": "RMZ Ecospace Tech Park", "pos": (50.0, 0.0, -50.0), "has_signal": True, "feeder": "FEEDER_BEL"},
        "INT_BEL_2": {"zone": "Zone_C", "name": "Bellandur Central Junction", "pos": (130.0, 0.0, -50.0), "has_signal": True, "feeder": "FEEDER_BEL"},
        "INT_BEL_3": {"zone": "Zone_C", "name": "Devarabeesanahalli Flyover", "pos": (50.0, 0.0, -130.0), "has_signal": True, "feeder": "FEEDER_BEL"},
        "INT_BEL_4": {"zone": "Zone_C", "name": "Kadubeesanahalli Underpass", "pos": (130.0, 0.0, -130.0), "has_signal": True, "feeder": "FEEDER_BEL"},

        # Silk Board
        "INT_SLK_1": {"zone": "Zone_D", "name": "Central Silk Board Main Signal", "pos": (-130.0, 0.0, -50.0), "has_signal": True, "feeder": "FEEDER_SLK"},
        "INT_SLK_2": {"zone": "Zone_D", "name": "Electronic City Flyover Ramp", "pos": (-50.0, 0.0, -50.0), "has_signal": True, "feeder": "FEEDER_SLK"},
        "INT_SLK_3": {"zone": "Zone_D", "name": "BTM 2nd Stage Connector", "pos": (-130.0, 0.0, -130.0), "has_signal": True, "feeder": "FEEDER_SLK"},
        "INT_SLK_4": {"zone": "Zone_D", "name": "Hosur Road Toll Entry", "pos": (-50.0, 0.0, -130.0), "has_signal": True, "feeder": "FEEDER_SLK"}
    }

    for iid, idata in intersections.items():
        G.add_node(iid, layer="traffic_intersection", **idata)

    def add_bidirectional_road(u: str, v: str, lanes: int = 3, length: float = 80.0, capacity: float = 1800.0):
        G.add_edge(u, v, layer="road", lanes=lanes, length=length, capacity=capacity, current_flow=0.0)
        G.add_edge(v, u, layer="road", lanes=lanes, length=length, capacity=capacity, current_flow=0.0)

    # Zone A internal grid
    add_bidirectional_road("INT_KOR_1", "INT_KOR_2")
    add_bidirectional_road("INT_KOR_3", "INT_KOR_4")
    add_bidirectional_road("INT_KOR_1", "INT_KOR_3")
    add_bidirectional_road("INT_KOR_2", "INT_KOR_4")

    # Zone B internal grid
    add_bidirectional_road("INT_HSR_1", "INT_HSR_2")
    add_bidirectional_road("INT_HSR_3", "INT_HSR_4")
    add_bidirectional_road("INT_HSR_1", "INT_HSR_3")
    add_bidirectional_road("INT_HSR_2", "INT_HSR_4")

    # Zone C internal grid
    add_bidirectional_road("INT_BEL_1", "INT_BEL_2")
    add_bidirectional_road("INT_BEL_3", "INT_BEL_4")
    add_bidirectional_road("INT_BEL_1", "INT_BEL_3")
    add_bidirectional_road("INT_BEL_2", "INT_BEL_4")

    # Zone D internal grid
    add_bidirectional_road("INT_SLK_1", "INT_SLK_2")
    add_bidirectional_road("INT_SLK_3", "INT_SLK_4")
    add_bidirectional_road("INT_SLK_1", "INT_SLK_3")
    add_bidirectional_road("INT_SLK_2", "INT_SLK_4")

    # Inter-Zone Arterial Expressways (The cascade spillover corridors)
    add_bidirectional_road("INT_KOR_2", "INT_HSR_1", lanes=3, length=80.0, capacity=1800.0)
    add_bidirectional_road("INT_KOR_4", "INT_HSR_3", lanes=3, length=80.0, capacity=1800.0)

    add_bidirectional_road("INT_HSR_3", "INT_BEL_1", lanes=4, length=80.0, capacity=2400.0)
    add_bidirectional_road("INT_HSR_4", "INT_BEL_2", lanes=4, length=80.0, capacity=2400.0)

    # Outer Ring Road (ORR) Bellandur to Silk Board
    add_bidirectional_road("INT_BEL_1", "INT_SLK_2", lanes=4, length=80.0, capacity=2600.0)
    add_bidirectional_road("INT_BEL_3", "INT_SLK_4", lanes=4, length=80.0, capacity=2600.0)

    # Hosur Road / Flyover Connector
    add_bidirectional_road("INT_SLK_1", "INT_KOR_3", lanes=3, length=80.0, capacity=2000.0)
    add_bidirectional_road("INT_SLK_2", "INT_KOR_4", lanes=3, length=80.0, capacity=2000.0)

    # BESCOM Power Layer
    G.add_node("BESCOM_CENTRAL_SUBSTATION", layer="power_substation", capacity_mva=100.0, voltage_kv=66.0, pos=(0.0, 0.0, 0.0))

    feeders = {
        "FEEDER_KOR": {"zone": "Zone_A", "capacity_mw": 16.0, "normal_load_mw": 9.2, "pos": (-80.0, 0.0, 80.0), "name": "BESCOM F-KOR 11kV"},
        "FEEDER_HSR": {"zone": "Zone_B", "capacity_mw": 13.5, "normal_load_mw": 7.8, "pos": (80.0, 0.0, 80.0), "name": "BESCOM F-HSR 11kV"},
        "FEEDER_BEL": {"zone": "Zone_C", "capacity_mw": 20.0, "normal_load_mw": 13.5, "pos": (80.0, 0.0, -80.0), "name": "BESCOM F-BEL 11kV (Ecospace)"},
        "FEEDER_SLK": {"zone": "Zone_D", "capacity_mw": 15.0, "normal_load_mw": 10.2, "pos": (-80.0, 0.0, -80.0), "name": "BESCOM F-SLK 11kV (Silk Board)"}
    }

    for fid, fdata in feeders.items():
        G.add_node(fid, layer="power_feeder", **fdata)
        G.add_edge("BESCOM_CENTRAL_SUBSTATION", fid, layer="transmission_line", capacity_mw=30.0)

    for iid, idata in intersections.items():
        feeder = idata["feeder"]
        G.add_edge(feeder, iid, layer="power_dependency", critical=True)

    return G


class InfrastructureTopology:
    """Wrapper class providing topological analysis and cascade paths."""

    def __init__(self):
        self.graph = build_city_graph()

    def get_zone_intersections(self, zone_id: str) -> List[str]:
        return [n for n, d in self.graph.nodes(data=True) if d.get("layer") == "traffic_intersection" and d.get("zone") == zone_id]

    def get_feeder_intersections(self, feeder_id: str) -> List[str]:
        return [v for u, v, d in self.graph.out_edges(feeder_id, data=True) if d.get("layer") == "power_dependency"]

    def get_adjacent_zones(self, zone_id: str) -> List[str]:
        adjacency = {
            "Zone_A": ["Zone_B", "Zone_D"],
            "Zone_B": ["Zone_A", "Zone_C"],
            "Zone_C": ["Zone_B", "Zone_D"],
            "Zone_D": ["Zone_A", "Zone_C"]
        }
        return adjacency.get(zone_id, [])

    def compute_spillover_impedance(self, congested_zone: str) -> Dict[str, float]:
        adj = self.get_adjacent_zones(congested_zone)
        weights = {"Zone_A": 0.35, "Zone_B": 0.45, "Zone_C": 0.65, "Zone_D": 0.85}
        return {neighbor: weights.get(neighbor, 0.5) for neighbor in adj}
