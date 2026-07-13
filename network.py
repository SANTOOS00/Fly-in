from networknode import Drones, Start_hub, List, End_hub, Connection, Hub
from collections import defaultdict


class FlightNetwork:
    def __init__(self) -> None:
        self.drones: Drones = None
        self.hubs: List[Hub, Start_hub, End_hub] = []
        self.connections: List[Connection] = []


class NetworkTopologyBuilder:
    def __init__(self) -> None:
        self.network_link: dict[str: list[Connection]] = {}

    def build(self, network: FlightNetwork) -> None:
        pass
