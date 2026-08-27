from typing import List
from graph import Graph
from modules import Hub, Edge


class Drone:
    def __init__(self, id: int, hub_current: Hub | None) -> None:
        """Initializes the FlyinError exception
            Args:
                messge (str)= 
                context (str)=
        """
        self.id: int = id
        self.current_hub: Hub | None = hub_current
        self.current_edge: Edge | None = None
        self.hub_next: Hub | None = None
        self.hub_visited: List[Hub | None] = [hub_current]
        self.edge_turns: int = 0

    def is_drone_on_edge(self) -> bool:
        if self.current_edge is None:
            return False
        return True

    def get_path_visited(self) -> List[Hub | None]:
        return self.hub_visited

    def get_current_hub(self) -> Hub | None:
        return self.current_hub

    def move(self, hub_next: Hub | None,
             graph: Graph) -> None:
        if hub_next is not None:
            self.hub_visited.append(hub_next)
            edge: Edge | None = graph.get_edge(self.current_hub, hub_next)
            self.update_hub_progress(hub_next, edge)
        else:
            self.update_edge_progress()

    def update_hub_progress(self,
                            hub_next: Hub | None,
                            edge: Edge | None
                            ) -> None:
        if edge is None:
            return
        edge.increment_usage_count()
        if hub_next is None:
            return
        if hub_next.zone.value == 1.0:
            self.entre_drone_hub(hub_next)
        else:
            self.entre_drone_edge(hub_next, edge)

    def entre_drone_edge(self, hub_next: Hub,
                         edge: Edge) -> None:
        if self.current_hub is None:
            raise ValueError(
                f"Drone {self.id} is not currently attached to any hub.")
        self.current_hub.increase_zone_size(self.id)
        self.current_edge = edge
        edge.decrease_edge_capacity(self.id)
        self.hub_next = hub_next
        hub_next.decrease_zone_size(self.id)
        self.add_edge_turn()

    def update_edge_progress(self) -> None:
        if self.hub_next is None:
            return
        if self.hub_next.get_zone_value() <= float(self.edge_turns + 1):
            self.current_hub = self.hub_next
            if self.current_edge is None:
                return
            self.current_edge.increase_edge_capacity(self.id)
            self.current_edge = None
            self.reset_edge_turn()
        else:
            self.add_edge_turn()

    def entre_drone_hub(self, hub_next: Hub | None) -> None:
        if hub_next is None:
            return
        self.entre_hub(hub_next)
        self.reset_edge_turn()

    def entre_hub(self, hub_next: Hub) -> None:
        if self.current_hub is None:
            return
        self.current_hub.increase_zone_size(self.id)
        self.current_hub = hub_next
        hub_next.decrease_zone_size(self.id)

    def add_edge_turn(self) -> None:
        self.edge_turns += 1

    def reset_edge_turn(self) -> None:
        self.edge_turns = 0
