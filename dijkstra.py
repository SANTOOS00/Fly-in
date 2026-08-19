import heapq as queue
from typing import List, Dict, Tuple
from modules import Hub, Adj_List
from map import Map

class Dijkstra:
    def __init__(self) -> None:
        self.paths: Dict[Hub, Hub] = {}
        self.heap = []
        self.distances = {}

    def run(self,
            graph: Adj_List,
            start_hub: Hub,
            end_hub: Hub
            ) -> List[Hub] | None:
        heap: List[Tuple[float, Hub]] = [(0.0, start_hub)]
        self._set_vertex_inf(start_hub)
        while heap:
            cost, hub_new = queue.heappop(heap)
            if end_hub == hub_new:
                return self.get_path(start_hub)
            for neighbor_hub, _ in graph[hub_new]:
                new_cost: float = cost + neighbor_hub.get_zone_value()
                if new_cost < self.distances[neighbor_hub.name]:
                    queue.heappush(heap, (new_cost, neighbor_hub))
                    self.distances[neighbor_hub.name] = new_cost
                    self.paths[neighbor_hub] = hub_new
        return None
        
    def get_path(self, start_hub: Hub) -> List[Hub]:
        path: List[Hub] = []
        sourch: Hub = Map().get_end()
        while sourch != start_hub:
            path.append(sourch)
            sourch = self.paths[sourch]
        path.append(sourch)
        path.reverse()
        return path

    def _set_vertex_inf(self, start: Hub) -> None:
        hubs = Map().hubs
        self.distances: Dict[str, float] = {name_hub: float('inf') for name_hub in hubs.keys()}
        self.distances[start.name] = 0
