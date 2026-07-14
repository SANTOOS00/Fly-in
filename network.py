from networknode import Drones, Start_hub, List, End_hub, Connection, Hub
from collections import defaultdict

class FlightNetwork:
    def __init__(self) -> None:
        self.drones: Drones = None
        self.hubs: List[Hub, Start_hub, End_hub] = []
        self.connections: List[Connection] = []


class NetworkTopologyBuilder:
    def __init__(self) -> None:
        self.network_link = defaultdict(list)

    def populate_network_links(self, network: FlightNetwork) -> None:
        for zone_1 in network.connections:
            edgs = list(zone_1.connection)
            self.network_link[edgs[0]].append(edgs[1])
            self.network_link[edgs[1]].append(edgs[0])
            