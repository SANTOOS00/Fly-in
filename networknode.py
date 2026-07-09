from typing import Protocol, List, Dict, Any
from custom_error import ErrorSeverity, HubError

class NetworkNode(Protocol):
    ...


class Drones(NetworkNode):
    def __init__(self, number_drones: int) -> None:
        self.drones: List[Dict[str, Any]] = [
            {
                "id": num + 1,
                "name_zone": None,
                "zone_visited_path": [],
            }
            for num in range(number_drones)
            ]

class End_hub(NetworkNode):
    _number_line_start = None
    _instance: bool = False

    def __init__(self, name: str, y: int, x: int,
                meta: Dict[str, Any] | None = None,
                line_number: int | None = None) -> "Start_hub":
        if End_hub._instance:
            raise HubError(
                "Duplicate Start hub at lines "
                f"{Start_hub._instance._number_line_start} "
                f"and {line_number}. Only one is allowed.",
                line_number,
                ErrorSeverity.Error)
        End_hub._number_line_start = line_number
        End_hub._instance = True
        self.name = name
        self.y = y
        self.x = x
        self.meta = meta

class Start_hub(NetworkNode):
    _number_line_start = None
    _instance: bool = False

    def __init__(self, name: str, y: int, x: int,
                meta: Dict[str, Any] | None = None,
                line_number: int | None = None) -> "Start_hub":
        if Start_hub._instance:
            raise HubError(
                "Duplicate Start hub at lines "
                f"{Start_hub._instance._number_line_start} "
                f"and {line_number}. Only one is allowed.",
                line_number,
                ErrorSeverity.Error)
        Start_hub._number_line_start = line_number
        Start_hub._instance = True
        self.name = name
        self.y = y
        self.x = x
        self.meta = meta


class Hub(NetworkNode):
    def __init__(self, name: str, y: int, x: int,
                 meta: Dict[str, Any] | None = None
                 ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.meta: Dict[str: Any] | None = meta


class Connection(NetworkNode):
    def __init__(self, connection: set, meta) -> None:
        self.connection = connection
        self.meta = meta