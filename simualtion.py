from drones import Drone
from typing import List
from map import Map
from modules import Hub, Edge, Adj_List
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
            if drone.is_drone_on_edge():
                drone.move_to_hub_or_edge(None, self.graph)
                continue
            hub_next = self.get_next_valid_hub(drone)
            if not hub_next:
                continue
            drone.move_to_hub_or_edge(hub_next, self.graph)
            if self.graph.is_end_hub(hub_next):
                self.remove_drone(drone)

    def get_next_valid_hub(self, drone: Drone) -> Hub | None:
        adj_list: Adj_List = self.graph.get_copy_adj_list()
        hub_next: Hub | None = None
        while True:
            path = self.dijkstra.run(adj_list,
                                 drone.get_hub_new(),
                                 self.end_hub)
            if not path:
                return None
            if not self.check_is_valid_edge(path[0], path[1]) or not self.check_is_valid_hub_next(path[1]):
                self.graph.remve_edge_is_adj_list(adj_list, self.graph.get_edge(path[0], path[1]))
            else:
                hub_next = path[1]
                break
        return hub_next

    def check_is_valid_edge(self, from_hub: Hub, to_hub: Hub) -> bool:
        edge = self.graph.get_edge(from_hub, to_hub)
        if not edge.has_available_capacity():
            return True
        return False

    def check_is_valid_hub_next(to_hub: Hub) -> bool:
        if to_hub.is_full():
            return True
        return False
        
    def check_finished(self) -> bool:
        if len(self.drones) == 0:
            return False
        return True

    def remove_drone(self, drone: Drone) -> None:
        self.drones.remove(drone)



