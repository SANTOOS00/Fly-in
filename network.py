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
    
    def get_hub(self, key_hub: str) -> Hub:
        return self.hubs[key_hub]


class Drone():
    def __init__(self, id: int) -> None:
        self.id = id


class NetworkTopologyBuilder:
    def __init__(self) -> None:
        self.graph: Dict[Hub, List[tuple[Hub, Connection]]] = defaultdict(list)
    
    def get_graph(self) -> Dict[str, List[str]]:
        return self.graph

    def populate_network_links(self, network: FlightNetwork) -> None:
        for edg in network.connections:
            link: List[str] = list(edg.connection)
            self.graph[network.get_hub(link[0])].append((network.get_hub(link[1]), edg))
            self.graph[network.get_hub(link[1])].append((network.get_hub(link[0]), edg))


class PathFinder:
    def __init__(self, network: FlightNetwork) -> None:
        self.distances: Dict[Hub, int] = {vertex: float('inf') for vertex in network.hubs.values()}
        self.distances[network.start_hube] = 0

    def find_all_paths(self, graph: Dict[Hub, List[tuple[Hub, Connection]]], start, end) -> None:
        pass


    def Dijkstra(self, graph: Dict[Hub, List[tuple[Hub, Connection]]], start, end) -> None:
        import heapq
        pro_queue = [(0, start)]
        while True:
            cost, hub = heapq.heappop(pro_queue)

            if hub == end:
                break
            
            if cost > self.distances[hub]
            for cost_test, edgs in graph[hub]:
                weight = cost_test.meta['zone'].value
                test = cost + weight
                # print(edgs)
                print(self.vertices[edgs])
            break


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


# self.stack_vertex: List[str] = [start.name]
# data_path: List[Tuple] = []
# visidet = set()
# while True:
#     vertex_new = self.stack_vertex.pop()
#     if vertex_new == end.name and self.save_path():
#         break
#     if vertex_new in visidet:
#         continue
#     visidet.update([vertex_new])
#     for vertex in network[vertex_new]:
#         self.stack_vertex.append(vertex)
#         data_path.append((vertex, vertex_new))
# self.print_data(data_path)
