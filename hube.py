from dataclasses import dataclass, field
from enum import Enum
from typing import Union
@dataclass(frozen=True)
class Hub:
    name: str
    x: int = field(hash=False, compare=False)
    y: int = field(hash=False, compare=False)
    zone: "Hub.Zone" = field(hash=False, compare=False)
    max_drones: int = field(hash=False, compare=False, default=1)
    color: str = field(hash=False, compare=False, default='#FFFFFF')
    size_zone: int  = field(hash=False, compare=False, default=0)

    def __lt__(self, oth: 'Hub') -> bool:
        return self.zone.value < oth.zone.value

    def get_type_zone(self) -> int:
        return int(self.zone.value)

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
        RESTRICTED = 2
        PRIORITY = 1
        BLOCKED = float('inf')
        NORMAL = 1

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
                case _:
                    return None
    zone: Zone = Zone.NORMAL


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
