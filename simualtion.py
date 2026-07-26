from drones import Drone
from typing import List
from map import Map
from modules import Adj_List
from graph import Graph
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
        torn = 0
        while self.check_finished():
            self.track_drone_zones()
    def track_drone_zones(self) -> None:
        adj_list: Adj_List
        for drone in self.drones:
            if drone.drone_in_edge():
                print("is ok")
                drone.drone_inta9alt_ila_hub(None, self.graph)
                continue

            adj_list = self.graph.get_copy_adj_list()
            self.graph.remove_edge_visited(drone.path_visited, adj_list)
            path = self.dijkstra.run(adj_list,
                                     drone.get_hub_new(),
                                     Map().get_end())

            if not path:
                continue
            # print(type(path[1]))
            drone.drone_inta9alt_ila_hub(path[1], self.graph)
            # print("ll")
            if self.graph.is_end_hub(path[1]):
                self.remove_drone(drone)

    def check_finished(self) -> bool:
        if len(self.drones) == 0:
            return False
        return True

    def remove_drone(self, drone: Drone) -> None:
        self.drones.remove(drone)



