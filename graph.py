from typing import List, Dict, Optional
 
from hube import Hub
from edge import Edge
from custom_error import FlyinError


class Graph:
    _instance: Optional['Graph'] = None
    _initialized: bool = False

    def __new__(cls) -> 'Graph':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if Graph._initialized is True:
            return
        Graph._initialized = True
        self.number_drones: int = None
        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None
        self.hubs: Dict[str, Hub] = {}
        self.edges: List[Edge] = []

    @FlyinError.check_error(type_error="Duplicate Zone")
    def add_hub(self, hub: Hub) -> None:
        if self.hubs.get(hub.name):
            raise FlyinError('test',
                             line_number=str(FlyinError.get_number_line()))
        self.hubs[hub.name] = hub

    @FlyinError.check_error(type_error='tet')
    def set_start_hub(self, start_hub: Hub) -> None:
        if self.start_hub is not None:
            raise FlyinError('test',
                             line_number=str(FlyinError.get_number_line()))
        self.start_hub = start_hub
        self.add_hub(start_hub)
    
    @FlyinError.check_error(type_error='tesst')
    def set_end_hub(self, end_hub: Hub) -> None:
        if self.end_hub is not None:
            raise FlyinError('test',
                             line_number=str(FlyinError.get_number_line()))
        self.end_hub = end_hub
        self.add_hub(end_hub)
    
    @FlyinError.check_error(type_error='testsss')
    def add_egde(self, edge: Edge) -> None:
        self._init_edge_for_hub(edge)
        print(edge)
        if {edge.source, edge.destintion} in [{edg.source, edg.destintion}
                                              for edg in self.edges]:
            raise FlyinError("testsssssssssssss",
                             line_number=FlyinError.get_number_line())
        self.edges.append(edge)
    

    def _init_edge_for_hub(self, edge: Edge) -> None:
        edge.source = self.hubs[edge.source]
        edge.destintion = self.hubs[edge.destintion]

    def _get_source_hub(self, name_zone: str) -> Hub:
        return self.get_hub(name_zone)


    def _get_destination_hub(self, name_zone: str) -> Hub:
        return self.get_hub(name_zone)        

    @FlyinError.check_error(type_error="Zone not in valid hubs")
    def get_hub(self, name_zone: str) -> Hub:
        if self.hubs.get(name_zone) is None:
            raise FlyinError(f"Zone name '{name_zone}' is not defined "
                             "in the configuration file.",
                             line_number=str(FlyinError.get_number_line()))
        print(self.hubs)
        return self.hubs[name_zone]

    @FlyinError.check_error(type_error='test')
    def set_number_drones(self, number_drones: int) -> None:
        if self.number_drones is not None:
            raise FlyinError('test',
                             line_number=FlyinError.get_number_line())
        self.number_drones = number_drones

