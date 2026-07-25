
from hube import Hub
from typing import List
from edge import Edge
from graph import Graph


class Drone:
    def __init__(self, id: int, hub_new: Hub) -> None:
        self.id: int = id
        self.hub_new: Hub = hub_new
        self.path_visidet: List[Hub] = [hub_new]

    def drone_inta9alt_ila_hub(self,
                               hub: Hub,
                               edge: Edge,
                               graph: Graph) -> None:
        self.hub_new.size_zone -= 1
        