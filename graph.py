from typing import List
from collections import defaultdict
from modules import Hub, Edge, Adj_List
from map import Map


class GraphBuilder:
    def __init__(self) -> None:
        self.network: Adj_List = Adj_List(defaultdict(list))

    def init_adj_list(self) -> Adj_List:
        from map import Map
        edges = Map().edges
        for edge in edges:
            self.network[edge.destination].append((edge.source, edge))
            self.network[edge.source].append((edge.destination, edge))
        return self.network


class Graph:
    def __init__(self) -> None:
        self.star_hub = Map().get_start()
        self.network: Adj_List = GraphBuilder().init_adj_list()
        self.end_hub = Map().get_end()

    @staticmethod
    def reset_all_edge_usage_counts() -> None:
        edges = Map().edges
        for edge in edges:
            edge.reset_usage_count()

    @staticmethod
    def remve_edge_is_adj_list(adj_list: Adj_List,
                               hub_from: Hub | None,
                               hub_to: Hub | None) -> None:
        if hub_from is None or hub_to is None:
            return
        for hub, edge in adj_list[hub_from]:
            if hub == hub_to:
                adj_list[hub_from].remove((hub, edge))
        for hub, edge in adj_list[hub_to]:
            if hub == hub_from:
                adj_list[hub_to].remove((hub, edge))

    def get_copy_adj_list(self) -> Adj_List:
        copy_adj: Adj_List = Adj_List({
            hub: neighbors.copy()
            for hub, neighbors in self.network.items()
            })
        return copy_adj

    @staticmethod
    def remove_path_visidet_drone(adj_list: Adj_List,
                                  path: List[Hub | None]) -> None:
        for i, hub in enumerate(path):
            if hub is None:
                continue
            if len(path) > i + 1:
                Graph.remve_edge_is_adj_list(adj_list, hub, path[i + 1])

    def is_end_hub(self, hub: Hub) -> bool:
        return self.end_hub == hub

    def get_edge(self, from_hub: Hub | None, to_hub: Hub) -> Edge | None:
        if from_hub is None:
            return None
        for hub, edge in self.network[from_hub]:
            if hub == to_hub:
                return edge
        return None
