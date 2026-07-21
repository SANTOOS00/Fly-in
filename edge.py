from dataclasses import dataclass
from hube import Hub, field


@dataclass(frozen=True)
class Edge:
    source: Hub
    destintion: Hub
    max_link_capacity: int = field(hash=False, compare=False, default=1)
    size_edge: int = field(hash=False, compare=False, default=0)


 
