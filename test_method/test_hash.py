from enum import Enum








@dataclass(frozen=True, unsafe_hash=False)
class Hub:
    name: str
    max_drones: int = 1
    color: str = "white"
    zone: Zone = Zone.NORMAL
    type: Hub.Type = Type.REGULAR



    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hub):
            return NotImplemented
        return self.name == other.name