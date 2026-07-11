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
        connections = network.get_connections()
        for conn in connections:
            pass
