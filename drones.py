from hube import Hub, List


class Drone:
    def __init__(self, id: int, hub_new: Hub) -> None:
        self.id: int = id
        self.hub_new: Hub = hub_new
        self.path_visidet: List[Hub] = []
