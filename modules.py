from typing import List
from typing import NewType, Dict, Tuple
from enum import Enum


Adj_List = NewType('Adj_List', Dict["Hub", List[Tuple["Hub", "Edge"]]])


class Hub:
    def __init__(self, name: str, x: int, y: int) -> None:
        self.name = name
        x = x
        y = y
        self.zone: "Hub.Zone" = Hub.Zone.NORMAL
        self.max_drones: int = 1
        self.color: str = 'white'
        self.drones_new: List[int] = []

    def __lt__(self, oth: 'Hub') -> bool:
        if self.zone == self.Zone.PRIORITY:
            return True
        if oth.zone == oth.Zone.PRIORITY:
            return False
        return bool(self.zone.value < oth.zone.value)

    def __hash__(self) -> int:
        return hash(self.name)

    def get_zone_value(self) -> float:
        return float(self.zone.value)

    def is_full(self) -> bool:
        return bool(self.max_drones > len(self.drones_new))

    def increase_zone_size(self, id_d: int) -> None:
        if self.drones_new:
            self.drones_new.remove(id_d)

    def decrease_zone_size(self, id_d: int) -> None:
        self.drones_new.append(id_d)

    class Zone(Enum):
        NORMAL = 1
        PRIORITY = 1
        RESTRICTED = 2
        BLOCKED = float('inf')

        @classmethod
        def get_type_zone(cls, type_zone: str) -> 'Hub.Zone':
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
                    raise ValueError(f"Invalid zone type: {type_zone}")


class Edge:
    def __init__(self, source: Hub, destination: Hub) -> None:
        self.source = source
        self.destination = destination
        self.max_link_capacity: int = 1
        self.drones_new: List[int] = []
        self.usage_count: int = 0

    def reset_usage_count(self) -> None:
        self.usage_count = 0

    def increment_usage_count(self) -> None:
        self.usage_count += 1

    def has_available_capacity(self) -> bool:
        return self.max_link_capacity > len(self.drones_new) \
            and self.max_link_capacity > self.usage_count

    def decrease_edge_capacity(self, id_d: int) -> None:
        self.drones_new.append(id_d)

    def increase_edge_capacity(self, id_d: int) -> None:
        if self.drones_new:
            self.drones_new.remove(id_d)
