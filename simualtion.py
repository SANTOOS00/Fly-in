from drones import Drone
from typing import List
from map import Map
from modules import Hub, Adj_List
from graph import Graph
from dijkstra import Dijkstra
import json

class Valid_Json:
    @staticmethod
    def adj_list_to_dict(adj_list: Adj_List):
        result = {}
        for hub in adj_list.keys():
            result[hub.name] = []
            for hu_ss, _ in adj_list[hub]:
                result[hub.name].append({
                    'to': hub.name,
                    'from': hu_ss.name
                })
        return result

    def write_in_data(self, adj_list: Adj_List, name_file: str) -> None:
        with open(f"{name_file}.txt", "w") as fb:
            json.dump(self.adj_list_to_dict(adj_list), fb, indent=4)
class Simulation:
    def __init__(self) -> None:
        self.drones: List[Drone] = [
            Drone(id + 1, hub_new=Map().get_start())
            for id in range(Map().number_drones)
        ]
        self.graph = Graph()
        self.dijkstra = Dijkstra()
        self.end_hub: Hub = Map().get_end()
        self.adj_list: Adj_List | None = None

    
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
        adj_list = self.graph.get_copy_adj_list()
        ss = Valid_Json()
        ss.write_in_data(adj_list, 'file_adj')
        raise ValueError()
        # while True:
        hub_next: Hub | None = None
            
        # path = self.dijkstra.run(adj_list,
        #                         drone.get_hub_new(),
        #                         self.end_hub)
            # self.graph.remve_edge_is_adj_list(adj_list, path[0], path[1])
            # if not path:
            #     return None

            # if self.check_is_valid_edge(path[0], path[1]) or self.check_is_valid_hub_next(path[1]):
            #     print('is ok')
        #  or 
        #     return None
        # else:
        #     hub_next = path[1]
        #     # break
        # return hub_next

    def check_is_valid_edge(self, from_hub: Hub, to_hub: Hub) -> bool:
        edge = self.graph.get_edge(from_hub, to_hub)
        if not edge.has_available_capacity():
            return True
        return False



    @staticmethod
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



