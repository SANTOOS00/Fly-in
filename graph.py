from typing import List, Dict 
from hube import Hub
from edge import Edge
from custom_error import FlyinError
from parser import Parseline

class Network:
    _instnce: None = None

    def __new__(cls) -> 'Network':
        if cls._instnce is None:
            cls._instnce = super().__new__(cls)
        return cls._instnce

    def __init__(self) -> None:
        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None
        self.hubs: Dict[str, Hub] = {}
        self.edge: List[Edge] = []

    @FlyinError.check_error(type_error="Duplicate Zone")
    def add_hub(self, hub: Hub) -> None:
        if self.hubs.get(hub.name):
            raise FlyinError(f"The zone name {hub.name} must not be repeated in the "
                                "config file; you must change the name only,",
                                line_number=str(Parseline.line_number))
        self.hubs[hub.name] = hub

    def set_start_hub(self, start_hub: Hub) -> None:
        self.hubs.add(start_hub)
        self.start_hub = start_hub
    
    def set_end_hub(self, end_hub: Hub) -> None:
        self.hubs.add(end_hub)
        self.end_hub = end_hub
    
    def add_egde(self, edge: Edge) -> None:
        self.edge.append(edge)

    @FlyinError.check_error(type_error="Zone not in valid hubs")
    def get_hub(self, name_zone: str) -> Hub:
        if not self.hubs.get(name_zone):
            raise FlyinError(f"Zone name '{name_zone}' is not defined "
                             "in the configuration file.",
                             line_number=str(Parseline.line_number))
        return self.hubs[name_zone]
