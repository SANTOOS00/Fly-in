import heapq as queue
from hube import Hub
from typing import List, Dict, Tuple
from edge import Edge

class Dijkstra:
    def __init__(self) -> None:
        self.paths: Dict[Hub, Hub] = {}
        self.heap = []
    def run(self,
            graph: Dict[Hub, List[Tuple[Hub, Edge]]],
            start_hub: Hub,
            end_hub: Hub
            ) -> tuple[List[Hub], float]:
        heap: List[Tuple[int, Hub]] = []
        heap.append((0, start_hub))
        self._set_vertex_inf(graph, start_hub)
        while heap:
            cost, hub_new = queue.heappop(heap)
            if end_hub == hub_new:
                return self.get_path(end_hub)
            for neighbor_hub, _ in graph[hub_new]:
                new_cost: int = cost + self.get_hub_score(neighbor_hub)
                if new_cost < self.distances[neighbor_hub]:
                    queue.heappush(heap, (new_cost, neighbor_hub))
                    self.distances[neighbor_hub] = new_cost
                    self.paths[neighbor_hub] = hub_new
        return None

    def get_hub_score(self, hub: Hub) -> float:
        if hub.is_full():
            return float('inf')
        return hub.get_zone_value()
        
    def get_path(self, end_hub: Hub) -> List[Hub]:
        path: List = []
        sourch = end_hub
        while self.paths.get(sourch):
            path.insert(0, sourch)
            sourch = self.paths[sourch]
        path.insert(0, sourch)
        return path

    def _set_vertex_inf(self, graph: Dict[Hub, List[Tuple[Hub, Edge]]], start: Hub) -> None:
        self.distances: Dict[Hub, float] = {hub: float('inf') for hub in graph.keys()}
        self.distances[start] = 0
