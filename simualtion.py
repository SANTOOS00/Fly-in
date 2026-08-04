from drones import Drone
from typing import List
from map import Map
from modules import Hub, Adj_List
from graph import Graph
from dijkstra import Dijkstra
import json
from enum import Enum


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
            fb.write('\n')
            fb.write("====================================")
            fb.write("====================================")
            fb.write("====================================")
            fb.write("====================================")
            fb.write("====================================")
            fb.write("====================================")


class Simulation:
    class MoveType(Enum):
        IN_HUB = "HUB"
        ON_EDGE = "EDGE"

    def __init__(self) -> None:
        hub_current = Map().get_start()
        numb_of_drone = Map().number_drones
        self.drones: List[Drone] = [
            Drone(id + 1, hub_current=hub_current)
            for id in range(numb_of_drone)
        ]
        self.graph = Graph()
        self.dijkstra = Dijkstra()
        self.end_hub: Hub = Map().get_end()
        self.start_hub: Hub = Map().get_start()
        self.adj_list: Adj_List | None = None
        self.string_output: str = ''

    def run(self) -> None:
        torn = 0
        while self.check_finished():
            torn += 1
            self.track_drone_zones(torn)
            self._reduction_drones()
            break
            # print(self.test)
            # self.test = ''
        # print(torn)


    def _reduction_drones(self) -> None:
        self.drones = list(filter(lambda dron: dron is not None, self.drones))

    def track_drone_zones(self,torn) -> None:
        # ss = Valid_Json()
        # ss.write_in_data(self.graph.network, 'sss')
        for drone in self.drones:
            if not drone.is_drone_on_edge():
                hub_next = self.get_next_valid_hub(drone)
                if not hub_next:
                    self.print_drone_in_action(drone)
                    continue

                drone.move(hub_next, self.graph)
                self.print_drone_in_action(drone)

                # if self.graph.is_end_hub(hub_next):
                #     self.remove_drone(drone)



            # if drone.is_drone_on_edge():
            #     drone.move(None, self.graph)
            #     self.print_drone_in_action(drone)
            #     continue

            # if not hub_next:
            #     continue


    def print_drone_in_action(self, drone: Drone) -> None:
        if drone.get_current_hub() == self.start_hub:
            return None
        if drone.is_drone_on_edge():
            self.string_output += f' D{drone.id}-{drone.current_hub.name}-{drone.hub_next.name}'
        else:
            self.string_output += f' D{drone.id}-{drone.current_hub.name}'

    def get_next_valid_hub(self, drone: Drone) -> Hub | None:
        adj_list: Adj_List = self.graph.get_copy_adj_list()
        hub_next: Hub | None = None
        self.graph.remove_path_visidet_drone(adj_list,
                                             drone.get_path_visited())
        # ss = Valid_Json()
        # ss.write_in_data(adj_list, 'test_list_adj')
        while True:
            path, cost = self.dijkstra.run(adj_list,
                                    drone.get_current_hub(),
                                    self.end_hub)
            if not path:
                return None
            if (self.check_is_valid_edge(path[0], path[1])
                and self.check_is_valid_hub_next(path[1])):
                hub_next = path[1]
                break
            else:
                self.graph.remve_edge_is_adj_list(adj_list, path[0], path[1])
        return hub_next
    def check_is_valid_edge(self, from_hub: Hub, to_hub: Hub) -> bool:
        edge = self.graph.get_edge(from_hub, to_hub)
        if edge.has_available_capacity():
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
        index_drone = self.drones.index(drone)
        self.drones[index_drone] = None
        


