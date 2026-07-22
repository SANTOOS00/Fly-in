import heapq
from hube import Hub
from typing import List, Dict, Tuple
from edge import Edge
from collections import defaultdict
from map import Map

class Dijkstra:
    def __init__(self) -> None:
        self.distances: Dict[Hub, int]
        self.heap: List[int, Hub]
        self.paths: Dict[Hub, Hub] = {}
        
    def run(self,
            graph: Dict[Hub, List[Tuple[Hub, Edge]]],
            ) -> List[Hub]:
        self._init_data(graph)
        while self._check_len_heap() != 0:
            cost, hub_new = heapq.heappop(self.heap)
            if Map().get_end() == hub_new:
                break
            for ajarhub, edge in graph[hub_new]:
                desti: int = cost + ajarhub.zone
                if desti < self.distances[ajarhub]:
                    heapq.heappush(self.heap, (desti, ajarhub))
                    self.distances[ajarhub] = desti
                    self.paths[ajarhub] = hub_new
        # for destion, source in self.paths.items():
        #     print(destion)
        #     print(source)
        #     print()
        return self.get_path()
    def get_path(self) -> List[Hub]:
        path: List = []
        sourch = Map().get_end()
        print(sourch)
        while sourch is not None:
            path.insert(self.paths[sourch])
            sourch = self.paths[sourch]
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
        heapq.heappush(self.heap, (0, start))
