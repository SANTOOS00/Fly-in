from networknode import Drones, Start_hub, List, End_hub, Connection, Hub, Dict
from collections import defaultdict
from typing import Tuple
import heapq
from itertools import count

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
    
    def get_hubs(self) -> None:
        return [hub  for hub in self.hubs]

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


class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.counter = count()

    def push(self, priority, hub):
        heapq.heappush(self.heap, (priority, next(self.counter), hub))

    def pop(self):
        cost, _, vertex = heapq.heappop(self.heap)
        return cost, vertex

    def is_empty(self):
        return len(self.heap) != 0


class PathFinder:
    def __init__(self, network: FlightNetwork) -> None:
        self.distances: Dict[Hub, int] = {vertex: float('inf') for vertex in network.hubs.values()}
        self.distances[network.start_hube] = 0

    def find_all_paths(self, graph: Dict[Hub, List[tuple[Hub, Connection]]], start, end) -> None:
        pass


    def Dijkstra(self, graph: Dict[Hub, List[tuple[Hub, Connection]]], start, end) -> None:
        priority_queue = PriorityQueue()
        priority_queue.push(0, start)
        paths = {vertex: None for vertex in graph.keys()}
        while priority_queue.is_empty():
            cost, hub = priority_queue.pop()
            if hub == end:
                break
            if cost < self.distances[hub]:
                continue
            for vertex, edgs in graph[hub]:
                distance = edgs.meta['max_link_capacity'] + cost
                
                if distance < self.distances[vertex]:
                    self.distances[vertex] = distance
                    priority_queue.push(distance, vertex)
                    paths[vertex] = hub
        path = []
        current = end
        while current is not None:
            path.insert(0, current)
            current = paths[current]


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
