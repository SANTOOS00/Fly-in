from typing import List
from typing import NewType, Dict, Tuple
from enum import Enum


Adj_List = NewType('Adj_List', Dict["Hub", List[Tuple["Hub | None",
                                                      "Edge | None"]]])


class Hub:
    """Representation of a hub (node) in the map graph.

    Attributes:
        name: Human-readable hub identifier.
        zone: Zone enum indicating access priority and traversal weight.
        max_drones: Maximum number of drones allowed simultaneously in the hub.
        color: Display color name used for printing.
        drones_new: List of drone ids currently occupying or reserved
        for the hub.
    """

    def __init__(self, name: str, x: int, y: int) -> None:
        """Create a Hub instance.

        Args:
            name: Identifier for the hub.
            x: X coordinate (unused in logic but stored conceptually).
            y: Y coordinate (unused in logic but stored conceptually).
        """
        self.name = name
        self.x = x
        self.y = y
        self.zone: "Hub.Zone" = Hub.Zone.NORMAL
        self.max_drones: int = 1
        self.color: str = 'white'
        self.drones_new: List[int] = []

    def __lt__(self, oth: 'Hub') -> bool:
        """Less-than comparison used for prioritizing hubs.

        Priority hubs are considered less than others so they are preferred in
        ordering. Otherwise comparison falls back to numeric zone value.
        """
        if self.zone == self.Zone.PRIORITY:
            return True
        if oth.zone == oth.Zone.PRIORITY:
            return False
        return bool(self.zone.value < oth.zone.value)

    def __hash__(self) -> int:
        """Hash based on the hub name to allow use as dict keys."""
        return hash(self.name)

    def get_zone_value(self) -> float:
        """Return the numeric traversal cost/value associated with
        the hub zone.

        Returns:
            Floating-point representation of the zone value.
        """
        return float(self.zone.value)

    def is_full(self) -> bool:
        """Return True when the hub can accept more drones.

        Note: method name follows existing code; behavior returns True when
        available capacity exists (max_drones > current drones count).
        """
        return bool(self.max_drones > len(self.drones_new))

    def increase_zone_size(self, id_d: int) -> None:
        """Remove a drone id from the hub occupancy list if present.

        Args:
            id_d: Drone id to remove from occupancy.
        """
        if self.drones_new:
            self.drones_new.remove(id_d)

    def decrease_zone_size(self, id_d: int) -> None:
        """Append a drone id to the hub occupancy list.

        Args:
            id_d: Drone id to add to occupancy.
        """
        self.drones_new.append(id_d)

    class Zone(Enum):
        """Enumeration of hub zone types and their associated
        numeric values."""
        NORMAL = 1
        PRIORITY = 1
        RESTRICTED = 2
        BLOCKED = float('inf')

        @classmethod
        def get_type_zone(cls, type_zone: str) -> 'Hub.Zone':
            """Map a string type to the corresponding Zone enum member.

            Args:
                type_zone: Textual zone name (case-insensitive).

            Returns:
                Corresponding Hub.Zone enum member.

            Raises:
                ValueError: When the provided type_zone is not recognized.
            """
            match type_zone.upper():
                case "NORMAL":
                    return cls.NORMAL
                case "BLOCKED":
                    return cls.BLOCKED
                case "PRIORITY":
                    return cls.PRIORITY
                case "RESTRICTED":
                    return cls.RESTRICTED
                case _:
                    raise ValueError("[ERROR]: Invalid "
                                     f"zone type: {type_zone}")


class Edge:
    """Representation of a connection between two hubs.

    Attributes:
        source: Hub where the edge originates.
        destination: Hub where the edge leads.
        max_link_capacity: Maximum concurrent drones allowed on the link.
        drones_new: List of drone ids currently occupying the edge.
        usage_count: Counter of how many times the edge was considered in a
            single simulation turn.
    """

    def __init__(self, source: Hub, destination: Hub) -> None:
        """Create an Edge connecting source and destination hubs."""
        self.source = source
        self.destination = destination
        self.max_link_capacity: int = 1
        self.drones_new: List[int] = []
        self.usage_count: int = 0

    def reset_usage_count(self) -> None:
        """Reset the per-turn usage counter to zero."""
        self.usage_count = 0

    def increment_usage_count(self) -> None:
        """Increment the per-turn usage counter by one."""
        self.usage_count += 1

    def has_available_capacity(self) -> bool:
        """Return True when the edge can accept another drone.

        Capacity is available when both the current occupancy is below the
        max_link_capacity and the usage_count has not exceeded capacity.
        """
        return self.max_link_capacity > len(self.drones_new) \
            and self.max_link_capacity > self.usage_count

    def decrease_edge_capacity(self, id_d: int) -> None:
        """Reserve capacity on the edge for the given drone id.

        Args:
            id_d: Drone id to append to the occupancy list.
        """
        self.drones_new.append(id_d)

    def increase_edge_capacity(self, id_d: int) -> None:
        """Release capacity previously reserved by the given drone id.

        Args:
            id_d: Drone id to remove from the occupancy list (if present).
        """
        if self.drones_new:
            self.drones_new.remove(id_d)
