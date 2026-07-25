from typing import List
from graph import Graph
from hube import Hub

class Drone:
    def __init__(self, id: int, hub_new: Hub) -> None:
        self.id: int = id
        self.hub_new: Hub = hub_new
        self.path_visidet: List[Hub] = [hub_new]

    def drone_inta9alt_ila_hub(self,
                               hub_next: Hub,
                               graph: Graph) -> None:
        edge = graph.get_edge(self.hub_new, hub_next)
        
        if graph.is_end_hub(hub_next):
            pass