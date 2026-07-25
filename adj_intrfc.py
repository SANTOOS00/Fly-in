from typing import Dict, List, NewType
from hube import Hub
from edge import Edge

ADJ_LIST = NewType('ADJ_LIST', Dict[Hub, List[tuple[Hub, Edge]]])
