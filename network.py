from networknode import Drones, Start_hub, List, End_hub, Connection, Hub
from collections import defaultdict


class FlightNetwork:
    def __init__(self) -> None:
        self.drones: Drones = None
        self.hubs: List[Hub, Start_hub, End_hub] = []
        self.connections: List[Connection] = []

    def get_connections(self) -> List[set]:
        return [conn for conn in self.connections]


class NetworkTopologyBuilder:
    def __init__(self) -> None:
        self.network_link = defaultdict(list)

    def build(self, network: FlightNetwork) -> None:
        pass


from typing import Dict, List


class Zone:
    pass


class Edges:
    pass


adj_list = {
    Zone : {
        Edges: [{
            "to": "waypoint1",
            "max_link_capacity": 1
        }
        ]
    },
    "waypoint1": {
        "meta": {
            "color": "blue",
            "max_drones": 1,
            "zone": "normal"
        },
        "edges": [{
            "to": "waypoint2",
            "max_link_capacity": 1
         },
         {
            "to": "waypoint2",
            "max_link_capacity": 1
         },

        ]
    },
}
