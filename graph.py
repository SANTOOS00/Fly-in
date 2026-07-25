from hube import Hub
from edge import Edge
from map import Map
from typing import Dict, List, Tuple, cast
from collections import defaultdict
from dijkstra import Dijkstra
import heapq as queue

class GraphBuilder:
    def __init__(self) -> None:
        self.graph: Dict[Hub, List[tuple[Hub, Edge]]] = defaultdict(list)

    def init_graph(self) -> Dict[Hub, List[Tuple[Hub, Edge]]]:
        edges = Map().edges
        for edge in edges:
            self.graph[edge.destintion].append((cast(Hub, edge.source), edge))
            self.graph[edge.source].append((cast(Hub, edge.destintion), edge))
        return self.graph

class Graph:
    def __init__(self) -> None:
        self.graph: Dict[Hub, List[tuple[Hub, Edge]]] = GraphBuilder().init_graph()
        self.star_hub = Map().get_start()        
        self.end_hub = Map().get_end()

    def run(self) -> None:
        pass

    def romve_edge(self, edges: List[Hub]) -> None:
        pass















































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


