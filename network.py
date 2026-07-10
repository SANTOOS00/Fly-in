from networknode import Drones, Start_hub, List, End_hub, Connection, Hub


class Graph:
    def __init__(self) -> None:
        self.drones: Drones = None
        self.start_hub: Start_hub = None
        self.hubs: List[Hub] = []
        self.end_hub: End_hub = None
        self.connections: List[Connection] = []

    def run(self) -> None:
        pass
