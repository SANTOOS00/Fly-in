from typing import List, Dict, Optional
from hube import Hub
from edge import Edge
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
        self.number_drones: int = None
        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None
        self.hubs: Dict[Hub, Hub] = {}
        self.edges: List[Edge] = []

    def get_start(self) -> Hub:
        return self.start_hub

    def get_end(self) -> None:
        return self.end_hub

    def add_hub(self, hub: Hub) -> Hub:
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
        self.add_hub(end_hub)
    
    def add_egde(self, edge: Edge) -> None:
        self._init_edge_for_hubs(edge)
        if {edge.source, edge.destintion} in [{edg.source, edg.destintion}
                                              for edg in self.edges]:
            raise FlyinError("testsssssssssssss", dd='add_edge',
                             line_number=FlyinError.get_number_line())
        self.edges.append(edge)    

    def _init_edge_for_hubs(self, edge: Edge) -> None:
        self._set_hub_source(edge)
        self._set_hub_destintion(edge)

    def _set_hub_source(self, edge: Edge) -> None:
        if self.hubs.get(edge.source):
            edge.source = self.hubs[edge.source]
        else:
            raise FlyinError("",
                             line_number=FlyinError.get_number_line())

    def _set_hub_destintion(self, edge: Edge) -> None:
        if self.hubs.get(edge.destintion):
            edge.destintion = self.hubs[edge.destintion]
        else:
            raise FlyinError("",
                             line_number=FlyinError.get_number_line())

    def _get_source_hub(self, name_zone: str) -> Hub:
        return self.get_hub(name_zone)


    def _get_destination_hub(self, name_zone: str) -> Hub:
        return self.get_hub(name_zone)        

    def get_hub(self, name_zone: str) -> Hub:
        if self.hubs.get(name_zone) is None:
            raise FlyinError(f"Zone name '{name_zone}' is not defined "
                             "in the configuration file.",
                             line_number=str(FlyinError.get_number_line()))
        print(self.hubs)
        return self.hubs[name_zone]

    def set_number_drones(self, number_drones: int) -> None:
        if self.number_drones is not None:
            raise FlyinError('test',
                             line_number=FlyinError.get_number_line())
        self.number_drones = number_drones

