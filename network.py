from networknode import Drones, Start_hub, List, End_hub, Connection, Hub, Dict
from collections import defaultdict

class FlightNetwork:
    def __init__(self) -> None:
        self.drones: Drones = None
        self.start_hube: Start_hub = None
        self.hubs: List[Hub, Start_hub, End_hub] = []
        self.end_hube: End_hub = None
        self.connections: List[Connection] = []
    
    def get_start(self) -> None:
        return self.start_hube

    def get_end(self) -> None:
        return self.end_hube

class Drone():
    def __init__(self, id: int) -> None:
        self.id = id


class NetworkTopologyBuilder:
    def __init__(self) -> None:
        self.network_link: Dict[str, List[str]] = defaultdict(list)

    def populate_network_links(self, network: FlightNetwork) -> None:
        for zone_1 in network.connections:
            edg = list(zone_1.connection)
            self.network_link[edg[0]].append(edg[1])
            self.network_link[edg[1]].append(edg[0])
    
    def get_network_link(self) -> Dict[str, List[str]]:
        return self.network_link


class PathFinder:
    def __init__(self) -> None:
        self.dict_paths = {}
        self.pths_save = []

    def find_all_paths(self, network: Dict[str, List[str]], start, end) -> None:
        stack_edgs: List[str] = [start.name]
        
        while True:
            vertex_new = stack_edgs.pop
            if vertex_new == end.name and self.save_path():
                break

    def save_path(self) -> None:
        print("is ok save path")
