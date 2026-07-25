from drones import Drone
from typing import List
from map import Map
from hube import Hub
from graph import Graph

class Simulation:
    def __init__(self, number_of_drones: int, start_hub: Hub) -> None:
        self.drones: List[Drone] = [
            Drone(id + 1, hub_new=start_hub)
            for id in range(number_of_drones)
        ]
        self.graph = Graph()

    def run(self) -> None:
        while self.check_finished():
            self.track_drone_zones()
            break
    def track_drone_zones(self) -> None:
        for drone in self.drones:
            print(drone.id)
            print(drone.hub_new)
    def check_finished(self) -> bool:
        if self.graph.end_hub.size_zone == len(self.drones):
            return False
        return True
