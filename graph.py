# from hub import Hub
from typing import List
from start_hub import Start_hub
from end_hub import End_hub
from connection import Connection
from hub import Hub
from drones import Drones


class Zone:
    def __init__(self) -> None:
        pass


class Graph:
    def __init__(self) -> None:
        self.drones: Drones = None
        self.start_hub: Start_hub = None
        self.hubs: List[Hub] = []
        self.end_hub: End_hub = None
        self.connections: List[Connection] = []

    def start_connected_zone(self) -> None:
        for hub in self.connections:
            print(hub.node1)
