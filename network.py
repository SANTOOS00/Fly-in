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


adj_list = {
    "name_zone": "zone_1",
    "data": [
        {
            "to": "zone_2",
            "meta": {
                "max_capacity": 2
            }
        }
    ],
    "zone_2": {
        "color": "red",
    },
    "data": [
        {
            "to": "zone_1",
            "meta": {
                "max_capacity": 2
            }
        },
        {
            "to": "zonr_3",
            "meta": {
                "max_capacity": 3
            }
        }
    ]
}


adj_list = {
    "start": {
        "meta": {
            "color": "green",
            "max_drones": 12,
            "zone": "normal"
        },
        "edges": [{
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
    "waypoint2": {
        "meta": {
            "color": "blue",
            "max drones": 1
        },
        "edges": [
            {
                "to": "waypoint1",
                "max_link_capacity": 1
            },
            {
                "to": "goal",
                "max_link_capcity": 1
            }
        ]
    },
    "goal": {
        "meta": {
            "color": "red",
            "max_drones": 1
        },
        "edges": [
            {
                "to": "waypoint1",
                "max_link_capackity": 1
            }
        ]
    }
}
