import heapq as queue
from hube import Hub
from typing import List, Dict, Tuple
from edge import Edge

class Dijkstra:
    def __init__(self) -> None:
        self.distances: Dict[Hub, int]
        self.paths: Dict[Hub, Hub] = {}

    def run(self,
            graph: Dict[Hub, List[Tuple[Hub, Edge]]],
            start_hub,
            end_hub
            ) -> List[Hub]:
        heap: List[int, Hub] = []
        heap.append((0, start_hub))
        self._set_distances_inf(graph, start_hub)
        while True:
            cost, hub_new = queue.heappop(heap)
            if end_hub == hub_new:
                break
            for ajarhub, _ in graph[hub_new]:
                desti: int = cost + ajarhub.zone
                if desti < self.distances[ajarhub]:
                    queue.heappush(heap, (desti, ajarhub))
                    self.distances[ajarhub] = desti
                    self.paths[ajarhub] = hub_new
        return self.get_path(end_hub)

    def get_path(self, end_hub: Hub) -> List[Hub]:
        path: List = []
        sourch = end_hub
        while self.paths.get(sourch):
            path.insert(0, sourch)
            sourch = self.paths[sourch]
        path.insert(0, sourch)
        return path

    def _check_len_heap(self) -> int:
        return len(self.heap)

    def _set_distances_inf(self, graph: Dict[Hub, List[Tuple[Hub, Edge]]], start: Hub) -> None:
        self.distances = {hub: float('inf') for hub in graph.keys()}
        self.distances[start] = 0
