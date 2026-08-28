from drones import Drone
from typing import List
from map import Map
from modules import Hub, Adj_List
from graph import Graph
from dijkstra import Dijkstra
from color import Color
from custom_error import FlyinError


class Simulation:
    """Run the drone movement simulation over the graph map.

    The Simulation object creates drones according to Map.number_drones and
    advances the system turn-by-turn until all drones have reached the end
    hub.
    """

    def __init__(self) -> None:
        """Initialize simulation state and helper components."""
        hub_current = Map().get_start()
        numb_of_drone = Map().number_drones
        self.drones: List[Drone | None] = [
            Drone(id + 1, hub_current=hub_current)
            for id in range(numb_of_drone)
        ]
        self.graph = Graph()
        self.dijkstra = Dijkstra()
        self.end_hub: Hub | None = Map().get_end()
        self.start_hub: Hub | None = Map().get_start()
        self.adj_list: Adj_List | None = None
        self.color = Color()

    def run(self) -> None:
        """Execute simulation turns until there are no active drones.

        The method validates that a path exists in the graph before the
        simulation loop and then iterates, advancing drone positions,
        printing status, and resetting per-turn edge usage counts.
        """
        torn = 0
        self.valid_graph_path()
        while self.check_finished():
            torn += 1
            self.track_drone_zones()
            self._reduction_drones()
            self.color.print_string()
            self.color.clear()
            self.graph.reset_all_edge_usage_counts()
        print(torn)

    def valid_graph_path(self) -> None:
        """Verify that at least one path exists from start to end.

        Raises:
            FlyinError: If no path is found in the graph.
        """
        adj_list: Adj_List = self.graph.get_copy_adj_list()
        if not adj_list:
            raise FlyinError("[ERROR]: The graph adjacency list is empty. "
                             "No hubs or connections found.")
        path: None | List[Hub] = self.dijkstra.run(adj_list,
                                                   self.start_hub,
                                                   self.end_hub)
        if path is None:
            raise FlyinError("[ERROR]: Unreachable target - no path "
                             "found in the graph.")

    def _reduction_drones(self) -> None:
        """Remove finished (None) drone slots from the internal list."""
        self.drones = list(filter(lambda dron: dron is not None, self.drones))

    def track_drone_zones(self) -> None:
        """Advance all drones by one simulation turn.

        For each drone the method determines if it should begin traversing a
        new edge or continue along the current edge, performs movement, and
        handles drone removal when reaching the end.
        """
        for drone in self.drones:
            if drone is None:
                break
            if not drone.is_drone_on_edge():
                hub_next = self.get_next_valid_hub(drone)
                if not hub_next:
                    self.print_drone_in_action(drone)
                    continue

                drone.move(hub_next, self.graph)
                self.print_drone_in_action(drone)

                if self.graph.is_end_hub(hub_next):
                    self.remove_drone(drone)
            else:
                drone.move(None, self.graph)
                self.print_drone_in_action(drone)

    def print_drone_in_action(self, drone: Drone) -> None:
        """Add a visual representation of the drone's action to the Color
        buffer.

        The method prints either the edge traversal (D<id>-HubA-HubB) or the
        hub location (D<id>-Hub). Drones at the start hub are omitted from
        output.
        """
        if drone.is_drone_on_edge():
            if drone.current_hub is None:
                return
            hub_a = self.color.join_color_string(
                drone.current_hub.name, drone.current_hub.color
            )
            if drone.hub_next is None:
                return
            hub_b = self.color.join_color_string(
                drone.hub_next.name, drone.hub_next.color
            )
            self.color.add(f' D{drone.id}-{hub_a}-{hub_b}')
        elif drone.get_current_hub() == self.start_hub:
            return None
        else:
            if drone.current_hub is None:
                return
            hub = self.color.join_color_string(
                drone.current_hub.name, drone.current_hub.color
            )
            self.color.add(f' D{drone.id}-{hub}')

    def get_next_valid_hub(self, drone: Drone) -> Hub | None:
        """Find the next valid hub for a drone using Dijkstra path searches.

        The function temporarily removes already visited hubs/edges for the
        drone and repeatedly searches for a shortest path. Candidate next
        hubs that pass edge and hub validity checks are collected and the
        best one is selected.
        """
        adj_list: Adj_List = self.graph.get_copy_adj_list()
        hub_next: List[Hub] = []
        self.graph.remove_path_visidet_drone(adj_list,
                                             drone.get_path_visited())
        while True:
            path = self.dijkstra.run(adj_list,
                                     drone.get_current_hub(),
                                     self.end_hub)
            if not path:
                break
            if (self.check_is_valid_edge(path[0], path[1]) and
                    self.check_is_valid_hub_next(path[1])):
                hub_next.append(path[1])
                self.graph.remve_edge_is_adj_list(adj_list, path[0], path[1])
                if len(hub_next) == 2:
                    break
            else:
                self.graph.remve_edge_is_adj_list(adj_list, path[0], path[1])
        return self.select_next_hub(hub_next)

    @staticmethod
    def select_next_hub(hub_nexts: List[Hub] | None) -> Hub | None:
        """Choose the preferred hub among candidates.

        Preference rules: when two candidates exist prefer the one with fewer
        drones already present; otherwise return the first candidate.
        """
        if hub_nexts is None:
            return None
        if len(hub_nexts) == 0:
            return None
        if len(hub_nexts) == 2 and len(hub_nexts[0].
                                       drones_new) > len(hub_nexts[1].
                                                         drones_new):
            return hub_nexts[1]
        return hub_nexts[0]

    def check_is_valid_edge(self, from_hub: Hub, to_hub: Hub) -> bool:
        """Return True when an edge between two hubs exists and has
        capacity."""
        edge = self.graph.get_edge(from_hub, to_hub)
        if edge is None:
            return False
        if edge.has_available_capacity():
            return True
        return False

    @staticmethod
    def check_is_valid_hub_next(to_hub: Hub) -> bool:
        """Return True when the destination hub can accept a drone.

        Note: method name follows existing code: `is_full` currently returns
        True when capacity exists.
        """
        if to_hub.is_full():
            return True
        return False

    def check_finished(self) -> bool:
        """Return True while there remain active drones in the simulation."""
        if len(self.drones) == 0:
            return False
        return True

    def remove_drone(self, drone: Drone) -> None:
        """Mark a drone as finished by replacing its slot with None.

        Args:
            drone: The Drone instance to mark as finished.
        """
        if drone in self.drones:
            index_drone = self.drones.index(drone)
            self.drones[index_drone] = None
