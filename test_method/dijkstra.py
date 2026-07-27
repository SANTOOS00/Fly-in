





from parser import Parseline
from graph import GraphBuilder
from dijkstra import Dijkstra
from typing import List
from hube import Hub

if __name__ == "__main__":
    ss = Parseline()
    ss.parse_file()
    graph = GraphBuilder().init_graph()
    path: List[Hub] = []
    path = Dijkstra().run(graph, Hub('waypoint1', 1, 2), Hub('goal', 1, 2))
    if not path:
        print('sss')
    for hu in path:
        print(hu.name)
