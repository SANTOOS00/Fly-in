from networknode import Drones, Start_hub, List, End_hub, Connection, Hub, Dict
from collections import defaultdict
from typing import Tuple

class FlightNetwork:
    def __init__(self) -> None:
        self.drones: Drones = None
        self.start_hube: Start_hub = None
        self.hubs: Dict[str: "name zone", Hub] = defaultdict()
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
        self.stack_vertex: List[str] = []
    def find_all_paths(self, network: Dict[str, List[str]], start, end) -> None:
        self.stack_vertex: List[str] = [start.name]
        data_path: List[Tuple] = []
        visidet = set()
        while True:
            vertex_new = self.stack_vertex.pop()
            if vertex_new == end.name and self.save_path():
                break
            if vertex_new in visidet:
                continue
            visidet.update([vertex_new])
            for vertex in network[vertex_new]:
                self.stack_vertex.append(vertex)
                data_path.append((vertex, vertex_new))
        self.print_data(data_path)

    def save_path(self) -> bool:
        if len(self.stack_vertex) == 0:
            return True
        return True


    def print_data(self, data):
        if isinstance(data, list):
            for d in data:
                print(d)
        if isinstance(data, dict):
            for key in data.keys():
                print(data[key])
