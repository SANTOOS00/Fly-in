from typing import List
from graph import Graph
from modules import Hub, Edge


class Drone:
    """Represent a drone moving between hubs on the graph.

    The Drone tracks its current hub/edge, visited hubs, and progress along
    an edge measured in `edge_turns`.
    """

    def __init__(self, id: int, hub_current: Hub | None) -> None:
        """Initialize a Drone.

        Args:
            id: Numeric identifier for the drone.
            hub_current: Initial Hub where the drone starts, or None.
        """
        self.id: int = id
        self.current_hub: Hub | None = hub_current
        self.current_edge: Edge | None = None
        self.hub_next: Hub | None = None
        self.hub_visited: List[Hub | None] = [hub_current]
        self.edge_turns: int = 0

    def is_drone_on_edge(self) -> bool:
        """Return True when the drone is currently traversing an edge.

        Returns:
            True if the drone has a non-None current_edge, False otherwise.
        """
        if self.current_edge is None:
            return False
        return True

    def get_path_visited(self) -> List[Hub | None]:
        """Get the list of hubs the drone has visited (including current).

        Returns:
            A list of Hub objects or None entries representing the visitation
            history.
        """
        return self.hub_visited

    def get_current_hub(self) -> Hub | None:
        """Return the hub at which the drone is currently located.

        Returns:
            The current Hub or None if the drone is on an edge.
        """
        return self.current_hub

    def move(self, hub_next: Hub | None,
             graph: Graph) -> None:
        """Advance the drone either onto the next hub or along its
            current edge.

        If hub_next is provided, the drone will append it to visited list and
        update hub/edge progress using the graph to resolve the edge. If
        hub_next is None, the drone continues traversing its current edge.

        Args:
            hub_next: Next hub to move to, or None to continue along edge.
            graph: Graph instance used to resolve edges between hubs.
        """
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
        """Handle entering or beginning traversal toward a neighboring hub.

        Args:
            hub_next: The hub being targeted or entered.
            edge: The Edge object representing the connection, or None.
        """
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
        """Begin traversing an edge toward `hub_next`.

        This updates zone sizes/capacity counters and marks the drone as on
        the edge.

        Args:
            hub_next: Destination hub reached when the edge traversal
                completes.
            edge: Edge being traversed.

        Raises:
            ValueError: If the drone is not currently attached to any hub.
        """
        if self.current_hub is None:
            raise ValueError(
                f"[ERROR]: Drone {self.id} is not currently attached to any hub.")
        self.current_hub.increase_zone_size(self.id)
        self.current_edge = edge
        edge.decrease_edge_capacity(self.id)
        self.hub_next = hub_next
        hub_next.decrease_zone_size(self.id)
        self.add_edge_turn()

    def update_edge_progress(self) -> None:
        """Advance progress along the current edge by one turn.

        When progress reaches the required value, the drone is placed at the
        next hub and edge capacities are restored.
        """
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
        """Enter a hub immediately (zone value == 1.0 case).

        Args:
            hub_next: Hub to enter. If None, no action is taken.
        """
        if hub_next is None:
            return
        self.entre_hub(hub_next)
        self.reset_edge_turn()

    def entre_hub(self, hub_next: Hub) -> None:
        """Move drone directly to `hub_next`, updating zone counters.

        Args:
            hub_next: Hub to move to.
        """
        if self.current_hub is None:
            return
        self.current_hub.increase_zone_size(self.id)
        self.current_hub = hub_next
        hub_next.decrease_zone_size(self.id)

    def add_edge_turn(self) -> None:
        """Increment the internal edge-turns counter by one."""
        self.edge_turns += 1

    def reset_edge_turn(self) -> None:
        """Reset the edge-turns counter to zero."""
        self.edge_turns = 0
