from hube import Hub, field, dataclass


@dataclass
class Edge:
    source: Hub | str
    destintion: Hub | str
    max_link_capacity: int = field(hash=False, compare=False, default=1)
    size_edge: int = field(hash=False, compare=False, default=0)


 
