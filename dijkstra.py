import heapq
from hube import Hub
from typing import List, Dict, Tuple
from edge import Edge
from map import Map

class Dijkstra:
    def __init__(self) -> None:
        self.distances: Dict[Hub, int]
        self.paths: Dict[Hub, Hub] = {}
        
    def run(self,
            graph: Dict[Hub, List[Tuple[Hub, Edge]]],
            start,
            end
            ) -> List[Hub]:
        heap: List[int, Hub] = []
        heapq.heappush(heap, (0, Map().get_start()))

        self._init_data(graph)
        while True:
            cost, hub_new = heapq.heappop(heap)
            if Map().get_end() == hub_new:
                break
            for ajarhub, _ in graph[hub_new]:
                desti: int = cost + ajarhub.zone
                if desti < self.distances[ajarhub]:
                    heapq.heappush(heap, (  desti, ajarhub))
                    self.distances[ajarhub] = desti
                    self.paths[ajarhub] = hub_new
        return self.get_path()

    def get_path(self) -> List[Hub]:
        path: List = []
        sourch = Map().get_end()
        while self.paths.get(sourch):
            path.insert(0, sourch)
            sourch = self.paths[sourch]
        path.insert(0, sourch)
        return path


    def _init_data(self,
                   graph: Dict[Hub, List[Tuple[Hub, Edge]]]) -> None:
        self._set_distances_inf(graph, Map().get_start())
        self._set_heap(Map().get_start())


    def _check_len_heap(self) -> int:
        return len(self.heap)

    def _set_distances_inf(self, graph: Dict[Hub, List[Tuple[Hub, Edge]]], start: Hub) -> None:
        self.distances = {hub: float('inf') for hub in graph.keys()}
        self.distances[start] = 0

    def _set_heap(self, start: Hub) -> None:
        self.heap = []
