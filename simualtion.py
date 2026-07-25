from drones import Drone
from typing import List
from map import Map
from hube import Hub
from graph import Graph, ADJ_LIST
from dijkstra import Dijkstra

class Simulation:
    def __init__(self) -> None:
        self.drones: List[Drone] = [
            Drone(id + 1, hub_new=Map().get_start())
            for id in range(Map().number_drones)
        ]
        self.graph = Graph()
        self.dijkstra = Dijkstra()

    def run(self) -> None:
        while self.check_finished():
            self.track_drone_zones()
            break
    def track_drone_zones(self) -> None:
        adj_list: ADJ_LIST
        for drone in self.drones:
            adj_list = self.graph.get_copy_adj_list()
            self.graph.remove_edge_visited(drone.path_visited, adj_list)
            if drone.test_name():
                drone.drone_inta9alt_ila_hub(path[1], self.graph)         
            path = self.dijkstra.run(adj_list,
                                     drone.hub_new,
                                     Map().get_end())
            if not path:
                continue
            drone.drone_inta9alt_ila_hub(path[1], self.graph)

    def check_finished(self) -> bool:
        if self.graph.end_hub.size_zone == len(self.drones):
            return False
        return True



