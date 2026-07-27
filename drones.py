from typing import List
from graph import Graph
from modules import Hub, Edge

class Drone:
    def __init__(self, id: int, hub_new: Hub) -> None:
        self.id: int = id
        self.hub_next: Hub | None = None
        self.path_visited: List[Hub] = [hub_new]
        self.current_hub: Hub | None = hub_new
        self.current_edge : Edge | None = None
        self.torne_moradart_edge : int = 0

    def update_edge_progress(self) -> None:
        if self.hub_next.get_zone_value() == self.torne_moradart_edge:
            self.hub_next.increase_zone_size()
            self.entre_hub(self.hub_next)
            self.current_edge = None
            self._reset_edge_turns()
        else:
            self._add_edge_turn()

    def update_hub_progress(self, hub_next: Hub, edge: Edge) -> None:
        if hub_next.get_zone_value() == 1:
            
            self.current_hub.decrease_zone_size()
            self.path_visited.append(self.current_hub)
            self.entre_hub(hub_next)
            hub_next.increase_zone_size()
            self._reset_edge_turns()

        elif hub_next.get_zone_value() > 1:
    
            self.current_hub.decrease_zone_size()
            self.current_edge = edge
            self.set_hub_next(hub_next)
            self.current_hub = None
            self._add_edge_turn()

    def move_to_hub_or_edge(self, hub_next: Hub | None,
                               graph: Graph) -> None:
        if not hub_next:
            self.update_edge_progress()
        elif hub_next:
            edge = graph.get_edge(self.current_hub, hub_next)
            self.update_hub_progress(hub_next, edge)

    def set_hub_next(self, hub_next: Hub) -> None:
        self.hub_next = hub_next

    def get_hub_new(self) -> None:
        return self.current_hub

    def entre_hub(self, hub_next: Hub) -> None:
        self.current_hub = hub_next

    def _add_edge_turn(self) -> None:
        self.torne_moradart_edge += 1

    def _reset_edge_turns(self) -> None:
        self.torne_moradart_edge = 0

    def is_drone_on_edge(self) -> bool:
        if not self.current_edge:
            return False
        return True