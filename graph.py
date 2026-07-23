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
        self.graph: Dict[Hub, List[tuple[Hub, Edge]]]    = GraphBuilder().init_graph()
        self.paths = []
        self.dijkstra = Dijkstra()
        self.star_hub = Map().get_start()        
        self.end_hub = Map().get_end()

    def run(self) -> None:
        pass

    def find_all_paths(self) -> None:
        pass
        # path ,cost = self.dijkstra.run(self.graph,
        #                        self.star_hub,
        #                        self.end_hub)
        # queue.heappush(self.paths, (cost, len(path), path))
        # for k in range(1, 5):
        #     graph_cope = self.graph.copy()
        #     for hub in 
    

            # queue.heappush(paths, )






