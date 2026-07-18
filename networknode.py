from dataclasses import dataclass
from enum import Enum
from custom_error import FlyinError

@dataclass(frozen=True)
class Hub:
    name: str
    type: "Hub.Type" = None
    zone: "Hub.Zone" = None
    max_drones: int = 1
    color: str = '#FFFFFF'

    def __hash__(self) -> int:
        return hash(self.name)

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

    class Type(Enum):
        NORMAL_HUB = "Normal_hub"
        START_HUB = "Start_hub"
        END_HUB = "End_hub"

        @classmethod
        def get_type_hube(cls, type_str: str) -> "Hub.Type":
            match type_str.upper():
                case "START_HUB":
                    return cls.START_HUB
                case "END_HUB":
                    return cls.END_HUB
                case "HUB":
                    return cls.NORMAL_HUB
                case _:
                    raise FlyinError("Invalid hub type found during parsing.", type_error="invalid_hub_type")

    class Zone(Enum):
        PRIORITY = 1
        NORMAL = 1
        RESTRICTED = 2
        BLOCKED = float('inf')

        @classmethod
        def get_type_zone(cls, type_zone: str) -> "Hub.Zone":
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
                    raise FlyinError("Invalid zone type found during parsing.", type_error="invalid_zone_type")

Hub.type = Hub.Type.NORMAL_HUB
Hub.zone = Hub.Zone.NORMAL

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



@dataclass
class Edge:
    source: Hub
    destintion: Hub