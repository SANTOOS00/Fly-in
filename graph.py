from typing import List, Dict 
from hube import Hub
from edge import Edge
from custom_error import FlyinError


class Graph:
    instance: None = None

    def __new__(cls) -> 'Graph':
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.number_drones: int = None
        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None
        self.hubs: Dict[str, Hub] = {}
        self.edges: List[Edge] = []

    @FlyinError.check_error(type_error="Duplicate Zone")
    def add_hub(self, hub: Hub) -> None:
        if self.hubs.get(hub.name):
            raise FlyinError('',
                             line_number=str(FlyinError.get_number_line()))
        self.hubs.update({hub.name: hub})

    @FlyinError.check_error(type='test')
    def set_start_hub(self, start_hub: Hub) -> None:
        self.start_hub = start_hub
        if self.start_hub is not None:
            print("hamid")
        self.add_hub(start_hub)
    
    @FlyinError.check_error(type='test')
    def set_end_hub(self, end_hub: Hub) -> None:
        if self.end_hub is not None:
            print("hamid")
        self.end_hub = end_hub
        self.add_hub(end_hub)
    
    def add_egde(self, edge: Edge) -> None:
        if edge is self.edges:
            raise FlyinError('',
                             FlyinError.get_number_line)
        self.edge.append(edge)

    @FlyinError.check_error(type_error="Zone not in valid hubs")
    def get_hub(self, name_zone: str) -> Hub:
        if not self.hubs.get(name_zone):
            raise FlyinError(f"Zone name '{name_zone}' is not defined "
                             "in the configuration file.",
                             line_number=str(FlyinError.get_number_line()))
        return self.hubs[name_zone]
    
    @FlyinError.check_error(type='')
    def set_number_drones(self, number_drones: int) -> None:
        if self.number_drones is not None:
            print('duleckt zones')
        self.number_drones = number_drones

