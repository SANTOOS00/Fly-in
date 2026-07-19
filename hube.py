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

    class Zone(Enum):
        PRIORITY = 1
        NORMAL = 1
        RESTRICTED = 2
        BLOCKED = float('inf')

        @classmethod
        @FlyinError.check_error("invalid zone type")
        def get_type_zone(cls, type_zone: str) -> "Hub.Zone":
            from parser import Parseline
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
                    raise FlyinError("Invalid zone type found during parsing.",
                                     line_number=f'{Parseline.line_number}')
    zone = Zone.NORMAL


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
