from typing import List
from graph import Graph
from modules import Hub, Edge

class Drone:
    def __init__(self, id: int, hub_current: Hub) -> None:
        self.id = id
        self.current_hub: Hub | None = hub_current
        self.hub_next: Hub | None = None
        self.current_edge: Edge | None = None
        self.path_visited: List[Hub] = [hub_current]
        self.edge_turns: int = 0

    def update_edge_progress(self) -> None:
        if self.hub_next.get_zone_value() == self.edge_turns:
            self.hub_next.increase_zone_size()
            self.entre_hub(self.hub_next)
            self.current_edge = None
            self.reset_edge_turns()
        else:
            self.add_edge_turn()


    def entre_drone_hub(self, hub_next: Hub) -> None:
            self.current_hub.decrease_zone_size()
            self.path_visited.append(self.current_hub)
            self.entre_hub(hub_next)
            hub_next.increase_zone_size()
            self.reset_edge_turns()

    def entre_drone_edge(self, hub_next: Hub, edge : Edge) -> None:
            self.current_hub.decrease_zone_size()
            self.current_edge = edge
            self.hub_next = hub_next
            self.current_hub = None
            self.add_edge_turn()

    def update_hub_progress(self, hub_next: Hub, edge: Edge) -> None:
        if hub_next.get_zone_value() == 1:
            self.entre_drone_hub(hub_next)
        else:
            self.entre_drone_edge(hub_next, edge)

    def move(self, hub_next: Hub | None,
                               graph: Graph) -> None:
        
        if hub_next is None:
            self.update_edge_progress()
        else:
            edge = graph.get_edge(self.current_hub, hub_next)
            self.update_hub_progress(hub_next, edge)

    def set_hub_next(self, hub_next: Hub) -> None:
        self.hub_next = hub_next

    def get_current_hub (self) -> None:
        return self.current_hub

    def entre_hub(self, hub_next: Hub) -> None:
        self.current_hub = hub_next

    def add_edge_turn(self) -> None:
        self.edge_turns += 1

    def reset_edge_turns(self) -> None:
        self.edge_turns = 0

    def is_drone_on_edge(self) -> bool:
        if self.current_edge is None:
            return False
        return True