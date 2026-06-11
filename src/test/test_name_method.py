from typing import List, Dict, Any
from abc import ABC, abstractmethod
from simulation import Start_hub, Hub, End_hub, Drones
from .custom_error import ParsingError
from utils import get_hex, allowed_status


class Parsier_meta_data(ABC):
    def __init__(self, meta_data: str, number_line: int) -> None:
        self.meta_data = meta_data
        self.number_line = number_line

    @abstractmethod
    def parser_line(slef) -> Dict[str, Any]:
        pass

    def parser_meta_data(self, meta_string: str) -> Dict[str, str]:



class Drones_parsing(Parsier_meta_data):
    def __init__(self, meta_data: str, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> int:



class Start_hub_parsing(Parsier_meta_data):
    def __init__(self, meta_data: str, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> Start_hub:

    def parser_meta_data(self, string: str) -> Dict[str, Any]:



class Hub_parsing(Parsier_meta_data):
    def __init__(self, meta_data, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> Dict:


    def parser_meta_data(self, string: str) -> Dict[str, Any]:



class End_hub_parsing(Parsier_meta_data):
    def __init__(self, meta_data, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> Dict:


    def parser_meta_data(self, string: str) -> Dict[str, Any]:


class Connection_parsing(Parsier_meta_data):
    def __init__(self, meta_data, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> Dict:
        pass

    def parser_meta_data(self, meta_string):



class LineValidator:
    def __init__(self, name_file: str) -> None:


    def type_line(self, line_str: str) -> ParsingError:


    def parser_line(self) -> ParsingError:



class Parsing:
    def __init__(self, name_file: str) -> None:


    def parser_args(self) -> None:


    def append_hub(self, hub: Hub) -> None:
        self.hubs.append(hub)
        # print(hub.meta)
    def append_connection(self, connection: Connection) -> None:
        self.connections.append(connection)
