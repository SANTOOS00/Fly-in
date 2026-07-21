from itertools import count
import heapq
from hube import Hub
from typing import List, Dict
from edge import Edge
from graph import Graph


class Dijstra:
    def __init__(self, graph: Graph) -> None:
        self.distances: Dict[Hub, int] = {vertex: float('inf') for vertex in graph.hubs.values()}
        self.distances[graph.start_hube] = 0

    def run(self,
            graph: Dict[Hub, List[Edge]], start, end
            ) -> List[Hub]:

        heap = []
        heapq.heappush(heap, (0, start))
        paths = {vertex: None for vertex in graph.keys()}
        while True:
            cost, hub = heapq.heappop(heap)
            if hub == end:
                break
            if cost < self.distances[hub]:
                continue
            for edge in graph[hub]:
                if edge.max_link_capacity == 0:
                    continue
                distance = vertex.zone + cost
                
                if distance < self.distances[vertex]:
                    self.distances[vertex] = distance
                    heapq.heappush(heap, (distance, vertex))
                    paths[vertex] = hub
        path = []
        current = end
        while current is not None:
            path.insert(0, current)
            current = paths[current]
