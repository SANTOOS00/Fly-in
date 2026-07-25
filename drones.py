from typing import List
from graph import Graph
from hube import Hub
from edge import Edge 

class Drone:
    def __init__(self, id: int, hub_new: Hub) -> None:
        self.id: int = id
        self.hub_new: Hub = hub_new
        self.path_visited: List[Hub] = [hub_new]
        self.current_hub: Hub | None = hub_new
        self.current_edge : Edge | None = None
        
    def drone_inta9alt_ila_hub(self,
                               hub_next: Hub,
                               graph: Graph) -> None:


                



        edge = graph.get_edge(self.hub_new, hub_next)
         
        # if self.id in [id for id in to_edge.drones_on_edge]:
        #     to_edge.pop(self.id)
        # else:


        if graph.is_end_hub(hub_next):
            pass


    def test_name(self) -> bool:
        return self.is_edge