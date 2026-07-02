from typing import List, Dict, Any
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
import os
import sys
#|------------------------------------------------------------------|
#|            ----- custom errors in project ------                 |
#|------------------------------------------------------------------|

class Type_Error(Enum):
    Warning = "Warning"
    Error = "Error"


class BaseError(Exception, ABC):
    def __init__(self, message: str, number_line: int | None = None, type_error: Type_Error | None = None) -> None:
        self.message = message
        self.number_line = number_line
        self.type_error = type_error
        
    @abstractmethod
    def get_error(self) -> str:
        return f"[{self.type_error.value}] line {self.number_line}: {self.message}"


class PathError(BaseError):
    def __init__(self, message: str, type_error: Type_Error | None = None) -> None:
        super().__init__(message, None, type_error)
    
    def get_error(self) -> str:
        return f"[{self.type_error.value}]: {self.message}"



class HubError(BaseError):
    def __init__(self, message: str, number_line, type_error: Type_Error) -> None:
        super().__init__(message, number_line, type_error)
    

    def get_error(self):
        return super()._get_error()


class HubError(BaseError):
    def __init__(self, message: str, number_line: int, type_error: Type_Error) -> None:
        super().__init__(message, number_line, type_error)
    
    def get_error(self):
        return super()._get_error()

class ConnectionError(BaseError):
    def __init__(self, message: str, number_line: int, type_error: Type_Error) -> None:
        super().__init__(message, number_line, type_error)
    
    def get_error(self):
        return super()._get_error()


#|------------------------------------------------------------------|
#|          -----    parmeter in simulation   ------                |
#|------------------------------------------------------------------|




class Drones:
    def __init__(self, number_drones: int) -> None:
        self.drones: List[Dict[str, Any]] = [
            {
                "id": num + 1,
                "name_zone": None,
                "zone_visited_path": [],
            }
            for num in range(number_drones)
            ]


class End_hub:
    _instance: "End_hub" = None

    def __new__(cls, name: str, y: int, x: int, meta: Dict[str, Any] = None
                ) -> "End_hub":
        if cls._instance is not None:
            raise HubError()

        cls._instance = super().__new__(cls)
        cls._instance.name = name
        cls._instance.y = y
        cls._instance.x = x
        cls._instance.meta = meta
        return cls._instance



class Start_hub:
    _instance: "Start_hub" = None

    def __new__(cls, name: str, y: int, x: int, meta: Dict[str, Any] = None
                ) -> "Start_hub":
        if cls._instance is not None:
            raise HubError()

        cls._instance = super().__new__(cls)
        cls._instance.name = name
        cls._instance.y = y
        cls._instance.x = x
        cls._instance.meta = meta
        return cls._instance


class Hub:
    def __init__(self, name: str, y: int, x: int, meta: str | None = None
                 ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.meta: Dict[str: Any] | None = meta


class Connection:
    def __init__(self, node1, node2, meta):
        self.node1 = node1
        self.node2 = node2
        self.meta = meta




#|------------------------------------------------------------------|
#|                  -----    PARSER ARGS   ------                   |
#|------------------------------------------------------------------|


class BaseParser(ABC):
    def __init__(self, line_str: str) -> None:
        self.number_line: int = 0
        self.line_str: str = line_str
        self.errors: List = []

    def parser() -> None:
        pass


class MetaParser(BaseParser):
    def parser(self) -> None:
        pass


class DroneParser(BaseParser):
    def parser():
        pass


class ZoneWithCoordsParser(BaseParser):
    pass


class StartHubParser(ZoneWithCoordsParser, MetaParser):
    pass


class EndHubParser(ZoneWithCoordsParser, MetaParser):
    pass


class HubParser(ZoneWithCoordsParser, MetaParser):
    pass


class ConnectionParser(MetaParser):
    pass


class LineValidator:
    pass






class ConfigParser:
    def __init__(self, path_file: Path) -> None:
        self.valid_path = path_file

    @property
    def valid_path(self, path_file: Path) -> None:
        if not path_file.exists is not True:
            raise PathError(f"File not found: {path_file}", Type_Error.Error)
        if not os.access(path_file, os.R_OK):
             raise PathError(f"No read permission: {path_file}", Type_Error.Error)
        self.path = Path(path_file)


def main() -> None:
    name_test = ConfigParser(sys.argv[1])
    print(name_test.path)

if __name__ == "__main__":
    # try:
    main()
    # except Exception as error:
    #     print(error.get_error())
