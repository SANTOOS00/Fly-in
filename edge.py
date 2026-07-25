from hube import Hub
from typing import List

class Edge:
    def __init__(self, source: Hub, destintion: Hub) -> None:
        self.source = source
        self.destintion = destintion
        self.max_link_capacity: int = 1
        self.drones_on_edge: List[int] = []

    def has_available_capacity(self) -> bool:
        return self.max_link_capacity > len(self.drones_on_edge)

 
