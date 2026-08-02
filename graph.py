from typing import Any, List
from collections import defaultdict
from modules import Hub, Edge, Adj_List
from map import Map

class GraphBuilder:
    def __init__(self) -> None:
        self.network: Adj_List = defaultdict(list)

    def init_adj_list(self) -> Adj_List:
        from map import Map
        edges = Map().edges
        for edge in edges:
            self.network[edge.destination].append((edge.source, edge))
            self.network[edge.source].append((edge.destination, edge))
        return self.network


class Graph:
    def __init__(self) -> None:
        self.network: Adj_List = GraphBuilder().init_adj_list()
        self.star_hub = Map().get_start() 
        self.end_hub = Map().get_end()

    @staticmethod
    def reset_all_edge_usage_counts() -> None:
        edges = Map().edges
        for edge in edges:
            edge.reset_usage_count()

    @staticmethod
    def remve_edge_is_adj_list(adj_list: Adj_List, hub_from: Hub, hub_to: Hub) -> None:
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
    def remove_path_visidet_drone(adj_list: Adj_List, path: List[Hub]) -> None:
        for i, hub in enumerate(path):
            if len(path) > i + 1:
                Graph.remve_edge_is_adj_list(adj_list, hub, path[i + 1])

    def is_end_hub(self, hub: Hub) -> bool:
        return self.end_hub == hub

    def get_edge(self, from_hub: Hub, to_hub: Hub) ->  Edge | None:
        for hub, edge in self.network[from_hub]:
            if hub.name == to_hub.name:
                return edge
        return None














































    # def find_all_paths(self) -> List[Tuple[Hub]] | List:
    #     path ,cost = self.dijkstra.run(self.graph,
    #                            self.star_hub,
    #                            self.end_hub)
    #     if path is None:
    #         return []
    #     K = 3
    #     A = []
    #     A.append((path, cost))
    #     B = []
    #     for k in range(1, K):
    #         prave_path = A[k - 1]

    #         for i in range(len(prave_path) - 1):

    #             spur_node = prave_path[i]
    #             root_path = prave_path[:i + 1]
    #             cope_grap = self.graph.copy()

    #             for path_test in A:
    #                 p_path = path_test[0]
    #                 if len(p_path) > i and root_path == p_path[:i + 1]:
    #                     hub_1 = p_path[i]
    #                     hub_2 = p_path[i + 1]
    #                     self.delete_edge(hub_1, hub_2, cope_grap)


        
    #                     # print(cope_grap[hub_1])
    #         break

    # def delete_edge(hub_1: Hub, hub_2: Hub, graph: Dict[Hub, List[tuple[Hub, Edge]]]) -> None:
    #     list_edge_1 = graph[hub_1]
    #     list_edge_2 = graph[hub_2]
    #     for i, (hub, edge) in enumerate(list_edge_1):
    #         if {hub, hub_1} == {edge.source, edge.destintion}:
    #             graph[hub_1].remove(graph[hub_1][i])

    #     for hub, edge in list_edge_2:
    #         if {hub, hub_2} == {edge.source, edge.destintion}:
    #             graph[hub_2].remove(graph[hub_2][i])
                
    #         # for path_data in A:
    #         #     p_path = path_data[0]
    #         #     if len(p_path) > i and root_path == p_path[:i + 1]:
    #         #         u = p_path[i]
    #         #         v = p_path[i + 1]
    #         #         if u in working_graph and v in working_graph[u]:
    #         #             del working_graph[u][v]

            
            

    #     # for k in range(1, K):
    #     # K = 5


