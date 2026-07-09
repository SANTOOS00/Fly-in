from enum import Enum


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


COLOR_HEX = {
    Color.BLACK: "#000000",
    Color.RED: "#FF0000",
    Color.GREEN: "#00FF00",
    Color.YELLOW: "#FFFF00",
    Color.BLUE: "#0000FF",
    Color.MAGENTA: "#FF00FF",
    Color.CYAN: "#00FFFF",
    Color.WHITE: "#FFFFFF",
    Color.ORANGE: "#FFA500",
    Color.PURPLE: "#800080",
    Color.BROWN: "#A52A2A",
    Color.LIME: "#00FF00",
    Color.GOLD: "#FFD700",
    Color.MAROON: "#800000",
    Color.DARKRED: "#8B0000",
    Color.VIOLET: "#EE82EE",
    Color.CRIMSON: "#DC143C",
    Color.RAINBOW: "#FF69B4",
}

