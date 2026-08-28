import heapq as queue
from typing import List, Dict, Tuple
from modules import Hub, Adj_List
from map import Map


class Dijkstra:
    """Find the lowest-cost path between hubs using Dijkstra's algorithm.

    This class stores intermediate path and distance tables during a run and
    exposes methods to execute the search and reconstruct the resulting path.
    """

    def __init__(self) -> None:
        """Initialize internal path, distance, and heap storage.

        The dictionaries and heap are reset for each new Dijkstra run.
        """
        self.paths: Dict[Hub, Hub] = {}
        self.distances: Dict[str, float] = {}
        self.heap: List[Tuple[float, Hub | None]] = []

    def run(self,
            graph: Adj_List,
            start_hub: Hub | None,
            end_hub: Hub | None
            ) -> List[Hub] | None:
        """Find the lowest-cost path between two hubs.

        Args:
            graph: Graph adjacency list mapping a Hub to a list of (neighbor,
                edge) tuples. The algorithm uses neighbor hubs' zone values
                to compute traversal cost.
            start_hub: Hub where the search starts. If None, the run returns
                None.
            end_hub: Hub where the search ends. If reached, the path from
                start_hub to end_hub is reconstructed and returned.

        Returns:
            A list of Hub instances representing the ordered path from start
            to end, or None if no path exists or inputs are invalid.
        """

        self.heap = [(0.0, start_hub)]
        self._set_vertexs_inf(start_hub)
        while self.heap:
            cost, hub_new = queue.heappop(self.heap)
            if hub_new is None:
                continue
            if hub_new.max_drones == 0:
                continue
            if end_hub == hub_new:
                return self.get_path(start_hub)
            for neighbor_hub, edge in graph[hub_new]:
                new_cost: float = cost + neighbor_hub.get_zone_value()
                if edge.max_link_capacity == 0:
                    continue
                if new_cost < self.distances[neighbor_hub.name]:
                    queue.heappush(self.heap, (new_cost, neighbor_hub))
                    self.distances[neighbor_hub.name] = new_cost
                    self.paths[neighbor_hub] = hub_new
        return None

    def get_path(self, start_hub: Hub | None) -> List[Hub] | None:
        """Reconstruct the path from the start hub to the end hub
             stored in Map.

        Args:
            start_hub: Hub from which the path reconstruction begins. If None,
                returns None.

        Returns:
            Ordered list of Hub objects from start to end, or None when a hub
            is unavailable.
        """
        if start_hub is None:
            return None
        path: List[Hub] = []
        source: Hub | None = Map().get_end()
        if source is None:
            return None
        while source != start_hub:
            path.append(source)
            source = self.paths[source]
        path.append(source)
        path.reverse()
        return path

    def _set_vertexs_inf(self, start: Hub | None) -> None:
        """Reset all hub distances to infinity and set the start distance.

        Args:
            start: Hub from which the path search begins. If None, the
                function returns without changes.
        """
        if start is None:
            return
        hubs = Map().hubs
        self.distances = {name_hub: float('inf') for name_hub in hubs.keys()}
        self.distances[start.name] = 0
