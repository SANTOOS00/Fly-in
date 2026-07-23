from hube import Hub
from edge import Edge
from map import Map
from typing import Dict, List, Tuple
from collections import defaultdict
from dijkstra import Dijkstra
import heapq as queue

class GraphBuilder:
    def __init__(self) -> None:
        self.graph: Dict[Hub, List[Tuple[Hub, Edge]]] = defaultdict(list)

    def init_graph(self) -> Dict[Hub, List[Tuple[Hub, Edge]]]:
        edges = Map().edges
        for edge in edges:
            self.graph[edge.destintion].append((edge.source, edge))
            self.graph[edge.source].append((edge.destintion, edge))
        return self.graph


class Graph:
    def __init__(self) -> None:
        self.graph: Dict[Hub, List[Tuple[Hub, Edge]]]    = GraphBuilder().init_graph()
        self.paths = []
        self.dijkstra = Dijkstra()
        self.star_hub = Map().get_start()        
        self.end_hub = Map().get_end()

    def run(self) -> None:
        pass

    def find_all_paths(self) -> None:
        path, cost = self.dijkstra.run(self.graph,
                               self.star_hub,
                               self.end_hub)
        
        for k in range(1, 5):
            graph_cope = self.graph.copy()
            for hub in 






# class PathFinder:
#     def __init__(self, network: FlightNetwork) -> None:
#         self.distances: Dict[Hub, int] = {vertex: float('inf') for vertex in network.hubs.values()}
#         self.distances[network.start_hube] = 0

#     def find_all_paths(self, graph: Dict[Hub, List[tuple[Hub, Connection]]], start, end) -> None:
#         pass


#     def Dijkstra(self, graph: Dict[Hub, List[tuple[Hub, Connection]]], start, end) -> None:
#         priority_queue = PriorityQueue()
#         priority_queue.push(0, start)
#         paths = {vertex: None for vertex in graph.keys()}
#         while priority_queue.is_empty():
#             cost, hub = priority_queue.pop()
#             if hub == end:
#                 break
#             if cost < self.distances[hub]:
#                 continue
#             for vertex, edgs in graph[hub]:
#                 distance = edgs.meta['max_link_capacity'] + cost
                
#                 if distance < self.distances[vertex]:
#                     self.distances[vertex] = distance
#                     priority_queue.push(distance, vertex)
#                     paths[vertex] = hub
#         path = []
#         current = end
#         while current is not None:
#             path.insert(0, current)
#             current = paths[current]


#     def save_path(self) -> bool:
#         if len(self.stack_vertex) == 0:
#             return True
#         return True

#     def print_data(self, data):
#         if isinstance(data, list):
#             for d in data:
#                 print(d)
#         if isinstance(data, dict):
#             for key in data.keys():
#                 print(data[key])
