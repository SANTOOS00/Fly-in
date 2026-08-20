from typing import List, Dict, Optional
from modules import Hub, Edge
from custom_error import FlyinError


class Map:
    _instance: Optional['Map'] = None
    _initialized: bool = False

    def __new__(cls) -> 'Map':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if Map._initialized is True:
            return
        Map._initialized = True
        self.number_drones: int | None = None
        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None
        self.hubs: Dict[str, Hub] = {}
        self.edges: List[Edge] = []

    def get_start(self) -> Hub | None:
        return self.start_hub

    def get_end(self) -> Hub:
        return self.end_hub

    def add_hub(self, hub: Hub) -> None:
        if self.hubs.get(hub.name):
            raise FlyinError('test',
                             type_error="Duplicate Zone",
                             line_number=str(FlyinError.get_number_line()))
        self.hubs[hub.name] = hub

    def set_start_hub(self, start_hub: Hub) -> None:
        if self.start_hub is not None:
            raise FlyinError('test',
                             line_number=str(FlyinError.get_number_line()))
        self.start_hub = start_hub
        self.add_hub(start_hub)
    
    def set_end_hub(self, end_hub: Hub) -> None:
        if self.end_hub is not None:
            raise FlyinError('test',
                             line_number=str(FlyinError.get_number_line()))
        self.end_hub = end_hub
        self.end_hub.max_drones = float('inf')
        self.add_hub(end_hub)

    def add_egde(self, edge: Edge) -> None:
        if {edge.source, edge.destination} in [{edg.source, edg.destination}
                                              for edg in self.edges]:
            raise FlyinError("testsssssssssssss", dd='add_edge',
                             line_number=str(FlyinError.get_number_line()))
        self.edges.append(edge)

    def validate_hub_end_start(self) -> None:
        if self.start_hub is None:
            raise ValueError(
                "[Error]: Missing Start Hub! \n  You must define at least "
                "one start hub using this format:\n"
                "    >> start_hub: name_zone x y [key=val] <<",
                number_line=str(FlyinError.get_number_line())
            )
        if self.end_hub is None:
            raise FlyinError(
                "[Error]: Missing End Hub! \n  You must define at least "
                "one end hub using this format:\n"
                "     >> start_end: name_zone x y [key=val] <<",
                number_line=str(FlyinError.get_number_line())
            )
 
    def get_hub(self, name_zone: str) -> Hub:
        if not self.hubs.get(name_zone):
            raise FlyinError(f"Zone name '{name_zone}' is not defined "
                             "in the configuration file.",
                             line_number=str(FlyinError.get_number_line()))
        return self.hubs[name_zone]

    def set_number_drones(self, number_drones: int) -> None:
        if self.number_drones is not None:
            raise FlyinError('test',
                             line_number=str(FlyinError.get_number_line()))
        self.number_drones = number_drones

