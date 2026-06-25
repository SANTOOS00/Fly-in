# from hub import Hub
from typing import List
from start_hub import Start_hub
from end_hub import End_hub
from connection import Connection
from hub import Hub
from drones import Drones


class Path:
    def __init__(self, name: str) -> None:
        self.name_zone = name
        self.connected_zones: tuple[Hub] = tuple()

    def add_connected_zone(self, ins_hub: Hub) -> None:
        self.connected_zones.append(ins_hub)


class Graph:
    def __init__(self) -> None:
        self.drones: Drones = None
        self.start_hub: Start_hub = None
        self.hubs: List[Hub] = []
        self.end_hub: End_hub = None
        self.connections: List[Connection] = []

    def start_connected_zone(self) -> None:
        pass
