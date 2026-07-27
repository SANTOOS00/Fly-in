from drones import Drone
from typing import List
from map import Map
from modules import Hub
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
        self.end_hub: Hub = Map().get_end()

    def run(self) -> None:
        torn = 0
        while self.check_finished():
            torn += 1
            self.track_drone_zones()
        print(torn)
    def track_drone_zones(self) -> None:
        adj_list: Adj_List
        for drone in self.drones:
            if drone.drone_in_edge():
                drone.drone_inta9alt_ila_hub(None, self.graph)
                continue

            adj_list = self.graph.get_copy_adj_list()
            self.graph.remove_edge_visited(drone.path_visited, adj_list)
            path = self.check_hub_bossiple()
            if 
            print('=====================')
            print(drone.id)
            print('======================')
            if not path:
                continue
            print('---------------------')
            print(drone.id)
            for hub in path:
                print(hub.name)
            print('---------------------')

            drone.drone_inta9alt_ila_hub(path[1], self.graph)
            if self.graph.is_end_hub(path[1]):
                self.remove_drone(drone)

    def check_hub_bossiple(self, drone: Drone) -> Hub | None:
        adj_list: Adj_List

        while True:

            path = self.dijkstra.run(adj_list,
                                 drone.get_hub_new(),
                                 self.end_hub)
            if not path:
                return None
            if not self.check_is_move_valid(path[0], path[1]):
                return None
            
            return path[1]

    def check_is_move_valid(self, from_hub: Hub, to_hub: Hub) -> bool:
        if to_hub.is_full():
            return False
        edge = self.graph.get_edge(from_hub, to_hub)
        if edge.has_available_capacity():
            return True
        return False
        
        
    def check_finished(self) -> bool:
        if len(self.drones) == 0:
            return False
        return True

    def remove_drone(self, drone: Drone) -> None:
        self.drones.remove(drone)



