from typing import List
from typing import NewType, Dict
from enum import Enum
from typing import Union
 

class Hub:
    def __init__(self, name:str, x: int, y: int) -> None:
        self.name = name
        x = x
        y = y
        self.zone: "Hub.Zone" = Hub.Zone.NORMAL
        self.max_drones: int = 1
        self.color: str = '#FFFFFF'
        self.size_zone: int  = 0

    def __lt__(self, oth: 'Hub') -> bool:
        if self.zone == self.Zone.PRIORITY:
            return True
        if oth.zone == oth.Zone.PRIORITY:
            return False
        return self.zone.value < oth.zone.value

    def __hash__(self) -> int:
        return hash(self.name)

    def get_zone_value(self) -> float:
        return float(self.zone.value)

    def is_full(self) -> bool:
        return self.size_zone == self.max_drones

    def increase_zone_size(self) -> None:
        self.size_zone += 1

    def decrease_zone_size(self) -> None:
        self.size_zone -= 1


    class Color(Enum):
        BLACK = "black"
        RED = "red"
        GREEN = "green"
        YELLOW = "yellow"
        BLUE = "blue"
        MAGENTA = "magenta"
        CYAN = "cyan"
        WHITE = "white"
        ORANGE = "orange"
        PURPLE = "purple"
        BROWN = "brown"
        LIME = "lime"
        GOLD = "gold"
        MAROON = "maroon"
        DARKRED = "darkred"
        VIOLET = "violet"
        CRIMSON = "crimson"
        RAINBOW = "rainbow"

        @classmethod
        def get_hex(cls, type_color: str) -> str:
            try:
                c = cls(type_color.lower())
                return COLOR_HEX[c]
            except Exception:
                return '#FFFFFF'

    class Zone(Enum):
        NORMAL = 1
        PRIORITY = 1
        RESTRICTED = 2
        BLOCKED = float('inf')

        @classmethod
        def get_type_zone(cls, type_zone: str) -> Union['Hub.Zone', None]:
            match type_zone.upper():
                case "NORMAL":
                    return cls.NORMAL
                case "BLOCKED":
                    return cls.BLOCKED
                case "PRIORITY":
                    return cls.PRIORITY
                case "RESTRICTED":
                    return cls.RESTRICTED


COLOR_HEX = {
    Hub.Color.BLACK: "#000000",
    Hub.Color.RED: "#FF0000",
    Hub.Color.GREEN: "#00FF00",
    Hub.Color.YELLOW: "#FFFF00",
    Hub.Color.BLUE: "#0000FF",
    Hub.Color.MAGENTA: "#FF00FF",
    Hub.Color.CYAN: "#00FFFF",
    Hub.Color.WHITE: "#FFFFFF",
    Hub.Color.ORANGE: "#FFA500",
    Hub.Color.PURPLE: "#800080",
    Hub.Color.BROWN: "#A52A2A",
    Hub.Color.LIME: "#00FF00",
    Hub.Color.GOLD: "#FFD700",
    Hub.Color.MAROON: "#800000",
    Hub.Color.DARKRED: "#8B0000",
    Hub.Color.VIOLET: "#EE82EE",
    Hub.Color.CRIMSON: "#DC143C",
    Hub.Color.RAINBOW: "#FF69B4",
}


class Edge:
    def __init__(self, source: Hub, destination: Hub) -> None:
        self.source = source
        self.destination = destination
        self.max_link_capacity: int = 1
        self.size_edge = 0
        self.usage_count = 0

    def reset_usage_count(self) -> None:
        self.usage_count = 0

    def increment_usage_count(self) -> None:
        self.usage_count += 1

    def has_available_capacity(self) -> bool:
        return (
            self.max_link_capacity > self.size_edge and self.usage_count < self.max_link_capacity
                )

    def decrease_edge_capacity(self) -> None:
        self.size_edge -= 1

    def increase_edge_capacity(self) -> None:
        self.size_edge += 1




Adj_List = NewType('Adj_List', Dict[Hub, List[tuple[Hub, Edge]]])
