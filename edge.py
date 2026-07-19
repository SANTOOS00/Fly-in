from dataclasses import dataclass
from enum import Enum
from hube import Hub


@dataclass(frozen=True)
class Edge:
    source: Hub
    destintion: Hub
    max_link_capacity: int = 1
    size_edge: int = 0
        