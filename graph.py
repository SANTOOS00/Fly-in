from typing import List
from collections import defaultdict
from modules import Hub, Edge, Adj_List
from map import Map


class GraphBuilder:
    """Helper to build an adjacency list representation of the map.

    The GraphBuilder reads edges from the global Map and constructs an
    Adj_List where each hub maps to tuples of (neighbor_hub, edge).
    """

    def __init__(self) -> None:
        self.network: Adj_List = Adj_List(defaultdict(list))

    def init_adj_list(self) -> Adj_List:
        """Populate and return the adjacency list from Map edges.

        Returns:
            An Adj_List mapping each Hub to a list of (neighbor_hub, Edge)
            tuples representing the undirected graph.
        """
        from map import Map
        edges = Map().edges
        for edge in edges:
            self.network[edge.destination].append((edge.source, edge))
            self.network[edge.source].append((edge.destination, edge))
        return self.network


class Graph:
    """Graph convenience wrapper that provides adjacency utilities.

    Graph uses Map to locate the start and end hubs and exposes helpers to
    manipulate adjacency lists and query edges.
    """

    def __init__(self) -> None:
        """Initialize graph wrapper by building the adjacency list."""
        self.star_hub = Map().get_start()
        self.network: Adj_List = GraphBuilder().init_adj_list()
        self.end_hub = Map().get_end()

    @staticmethod
    def reset_all_edge_usage_counts() -> None:
        """Reset usage counters for every Edge in the Map."""
        edges = Map().edges
        for edge in edges:
            edge.reset_usage_count()

    @staticmethod
    def remve_edge_is_adj_list(adj_list: Adj_List,
                               hub_from: Hub | None,
                               hub_to: Hub | None) -> None:
        """Remove a bidirectional connection between two hubs from adj_list.

        Args:
            adj_list: Adjacency list to modify.
            hub_from: Source hub of the connection.
            hub_to: Destination hub of the connection.

        Notes:
            The function is a no-op when either hub is None. It removes the
            pair entries in both directions if present.
        """
        if hub_from is None or hub_to is None:
            return
        for hub, edge in adj_list[hub_from]:
            if hub == hub_to:
                adj_list[hub_from].remove((hub, edge))
        for hub, edge in adj_list[hub_to]:
            if hub == hub_from:
                adj_list[hub_to].remove((hub, edge))

    def get_copy_adj_list(self) -> Adj_List:
        """Return a shallow copy of the current adjacency list."""
        copy_adj: Adj_List = Adj_List({
            hub: neighbors.copy()
            for hub, neighbors in self.network.items()
            })
        return copy_adj

    @staticmethod
    def remove_path_visidet_drone(adj_list: Adj_List,
                                  path: List[Hub | None]) -> None:
        """Remove edges along a given path from the adjacency list.

        Args:
            adj_list: The adjacency list to modify.
            path: Sequence of hubs representing the path to remove.
        """
        for i, hub in enumerate(path):
            if hub is None:
                continue
            if len(path) > i + 1:
                Graph.remve_edge_is_adj_list(adj_list, hub, path[i + 1])

    def is_end_hub(self, hub: Hub) -> bool:
        """Return True when `hub` is the configured end hub.

        Args:
            hub: Hub to check.

        Returns:
            True if the provided hub equals the graph's end hub.
        """
        return self.end_hub == hub

    def get_edge(self, from_hub: Hub | None, to_hub: Hub) -> Edge | None:
        """Find and return the Edge connecting two hubs, if any.

        Args:
            from_hub: Hub from which the edge departs. If None, return None.
            to_hub: Destination Hub to look for.

        Returns:
            The Edge object if found, else None.
        """
        if from_hub is None:
            return None
        for hub, edge in self.network[from_hub]:
            if hub == to_hub:
                return edge
        return None
