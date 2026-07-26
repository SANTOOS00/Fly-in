import heapq as queue
from typing import List, Dict, Tuple
from modules import Hub, Adj_List

class Dijkstra:
    def __init__(self) -> None:
        self.paths: Dict[Hub, Hub] = {}
        self.heap = []
    def run(self,
            graph: Adj_List,
            start_hub: Hub,
            end_hub: Hub
            ) -> tuple[List[Hub], float]:
        heap: List[Tuple[int, Hub]] = []
        heap.append((0, start_hub))
        self._set_vertex_inf(graph, start_hub)
        while heap:
            cost, hub_new = queue.heappop(heap)
            if end_hub == hub_new:
                print("ss")
                return self.get_path(end_hub)
            for neighbor_hub, edge in graph[hub_new]:
                new_cost: int = cost + self.get_hub_score(neighbor_hub)
                if new_cost < self.distances[neighbor_hub] and edge.has_available_capacity():
                    queue.heappush(heap, (new_cost, neighbor_hub))
                    self.distances[neighbor_hub] = new_cost
                    self.paths[neighbor_hub] = hub_new
        return None

    def get_hub_score(self, hub: Hub) -> float:
        if hub.is_full():
            return float('inf')
        return hub.get_zone_value()
        
    # def get_path(self, end_hub: Hub) -> List[Hub]:
    #     path: List = []
    #     sourch = end_hub
    #     while self.paths.get(sourch):
    #         path.insert(0, sourch)
    #         # print('ss')
    #         sourch = self.paths[sourch]
    #     path.insert(0, sourch)
    #     return path
    def get_path(self, end_hub: Hub) -> List[Hub]:
        path: List[Hub] = []
        sourch = end_hub
        visited = set()

        while sourch in self.paths:
            if sourch in visited:
                print(f"[Error Cycle] Loop detected at hub: {sourch}")
                break
                
            visited.add(sourch)
            path.append(sourch)
            sourch = self.paths[sourch]

        path.append(sourch)
        path.reverse()  # قلب القائمة مرة واحدة في الأخير O(N)
        return path
    def _set_vertex_inf(self, graph: Adj_List, start: Hub) -> None:
        self.distances: Dict[Hub, float] = {hub: float('inf') for hub in graph.keys()}
        self.distances[start] = 0
