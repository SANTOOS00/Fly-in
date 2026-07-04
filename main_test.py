from typing import List, Dict, Any
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
import os
import sys
from typing import TextIO
from functools import singledispatchmethod
import re


class Type_Error(Enum):
    Warning = "Warning"
    Error = "Error"


class BaseError(Exception, ABC):
    """
    #|------------------------------------------------------------------|
    #|            ----- custom errors in project ------                 |
    #|------------------------------------------------------------------|
    """

    def __init__(self, message: str, number_line: int | None = None,
                 type_error: Type_Error | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.number_line = number_line
        self.type_error = type_error

    @abstractmethod
    def get_error(self) -> str:
        return (
            f"[{self.type_error.value}] line {self.number_line}: "
            f"{self.message}")


class PathError(BaseError):
    def __init__(self, message: str, type_error: Type_Error | None = None
                 ) -> None:
        super().__init__(message, type_error=type_error)

    def get_error(self) -> str:
        return f"[{self.type_error.value}]: {self.message}"


class HubError(BaseError):
    def __init__(self, message: str, number_line, type_error: Type_Error
                 ) -> None:
        super().__init__(message, number_line, type_error)

    def get_error(self):
        return super()._get_error()


class ConnectionError(BaseError):
    def __init__(self, message: str, number_line: int, type_error: Type_Error
                 ) -> None:
        super().__init__(message, number_line, type_error)

    def get_error(self):
        return super()._get_error()


class UtilsError(BaseError):
    def __init__(self, message: str, number_line: int | None = None,
                 type_error: Type_Error | None = None) -> None:
        super().__init__(message, number_line, type_error)

    def get_error(self):
        return super().get_error()


class Drones:
    """
    |------------------------------------------------------------------|
    |          -----    parmeter in simulation   ------                |
    |------------------------------------------------------------------|
    """
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

    def __new__(cls, name: str, y: int, x: int,
                meta: Dict[str, Any] | None = None
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

    def __new__(cls, name: str, y: int, x: int,
                meta: Dict[str, Any] | None = None
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
    def __init__(self, name: str, y: int, x: int,
                 meta: Dict[str, Any] | None = None
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


class BaseParser(ABC):
    """
    |------------------------------------------------------------------|
    |                  -----    PARSER ARGS   ------                   |
    |------------------------------------------------------------------|
    """
    def __init__(self, line_str: str, nu_line: int) -> None:
        self.nu_line: int = nu_line
        self.line_str: str = line_str

    @abstractmethod
    def parser(self) -> None:
        pass


class MetaParser:
    pass


class ZoneWithCoordsParser(BaseParser):
    def __init__(self, line_str: str, nu_line: int) -> None:
        super().__init__(line_str, nu_line)

    def parser(self) -> None:
        line = self.line.strip()
        if not line:
            return None

        pattern = r'^(\w+)\s+(\d+)\s+(\d+)\s+(\w+)'
        match = re.match(pattern, line)
        print(match)
        if match:
            name, x, y, options_raw = match.groups()
            # is_valid_x_and_y(x, y):
            return Hub(name, x, y, options_raw)


class DroneParser(BaseParser):
    def __init__(self, line_str: str, nu_line: int) -> None:
        super().__init__(line_str, nu_line)

    def parser(self) -> Drones:
        try:
            if int(self.raw_line) > 0:
                return Drones(int(self.raw_line))
            else:
                raise UtilsError("'nb_drones' value must be a valid integer.", 
                                 self.nu_line, Type_Error.Error)
        except ValueError:
            raise UtilsError("'nb_drones' value must be a valid integer.",
                             self.nu_line, Type_Error.Error)


class StartHubParser(ZoneWithCoordsParser, MetaParser):
    def __init__(self, line_str: str, nu_line: int) -> None:
        super().__init__(line_str, nu_line)

    def parser(self) -> Start_hub:
        print("is ok valid start")


class EndHubParser(ZoneWithCoordsParser, MetaParser):
    def __init__(self, line_str: str, nu_line: int) -> None:
        super().__init__(line_str, nu_line)

    def parser(self) -> End_hub:
        print("is ok valid End")


class HubParser(ZoneWithCoordsParser, MetaParser):
    def __init__(self, line_str: str, nu_line: int) -> None:
        super().__init__(line_str, nu_line)

    def parser(self) -> Hub:
        print("is ok valid hub")


class ConnectionParser:
    def __init__(self, line_str: str, nu_line: int) -> None:
        self.line_str = line_str
        self.nu_line = nu_line

    def parser(self) -> Connection:
        Connection("name_zone_end", "name_zone_start", "[dd]")


class SafeFileReader:
    def __init__(self, path_file: Path) -> None:
        self.valid_path: Path = path_file
        self.number_line: int = 0

    @property
    def valid_path(self) -> Path:
        return self._fd

    @valid_path.setter
    def valid_path(self, path_file: Path) -> None:
        if not path_file.exists():
            raise PathError(
                f"File not found: {path_file}", Type_Error.Error)
        if not os.access(path_file, os.R_OK):
            raise PathError(
                f"No read permission: {path_file}", Type_Error.Error)
        self._fd: TextIO = open(path_file, encoding="utf-8")

    def get_validated_line(self) -> Dict[str, str] | str:
        while True:
            raw_line = self._fd.readline()
            if not raw_line:
                return "EOF"
            self.number_line += 1
            self.data_str = raw_line.split("#", maxsplit=1)[0].strip()
            if self.data_str == "":
                continue
            if self._get_type_line():
                parser_component = self.key(self.val, self.number_line)
                return (parser_component.parser())
            else:
                raise UtilsError(
                    f"Unknown configuration token '{self.key}'",
                    self.number_line, Type_Error.Error)

    def __del__(self) -> None:
        self._fd.close()

    def _get_type_line(self) -> bool:
        if self.data_str.count(":") != 1:
            raise UtilsError(
                "The line type must match one of the allowed formats "
                "{nb_drones, start_hub, etc.}. Example: [type: ,,, ]",
                self.number_line, Type_Error.Error)
        key_raw, self.val = self.data_str.split(":", 1)
        key = key_raw.lower()
        parsers = {
            "nb_drones": DroneParser,
            "start_hub": StartHubParser,
            "hub": HubParser,
            "end_hub": EndHubParser,
            "connection": ConnectionParser
        }
        if parsers.get(key):
            self.key = parsers[key]
            return True
        return False


class Graph:
    def __init__(self) -> None:
        self.drones: Drones = None
        self.start_hub: Start_hub = None
        self.hubs: List[Hub] = []
        self.end_hub: End_hub = None
        self.connections: List[Connection] = []


class ParserConfig:
    def __init__(self) -> None:
        self.errors: List[str] | None = []
        self.graph = Graph()
 
    def parse_in_type_line(self) -> None:
        fileread = SafeFileReader(Path(sys.argv[1]))
        while (True):
            try:
                component = fileread.get_validated_line()
                if component == "EOF":
                    print("sss")
                    break
                print(component)
                self.update_graph(component)
            except Exception as error:
                if isinstance(error, BaseError):
                    self.errors.append(error.get_error())
                else:
                    print(error)
        self.print_report()

    def print_report(self) -> None:
        if self.errors:
            string_error = ""
            print(f"\n💥 Found {len(self.errors)} Error(s) in "
                  "configuration file:", file=sys.stderr)
            for error in self.errors:
                string_error += (f" ⚠️  + {error}\n")
            string_error += ("\n❌ Pipeline Status: FAILED\n")
            raise UtilsError(string_error)

    @singledispatchmethod
    def update_graph(self, data):
        raise UtilsError(
                    f"Unknown configuration token '{data}'",
                    self.number_line, Type_Error.Error)

    @update_graph.register(Drones)
    def _(self, component: Drones):
        self.graph.drones = component

    @update_graph.register(Hub)
    def _(self, component: Hub) -> None:
        self.graph.hubs.append(component)

    @update_graph.register(Start_hub)
    def _(self, component: Start_hub):
        self.graph.start_hub = component

    @update_graph.register(End_hub)
    def _(self, component: End_hub):
        self.graph.end_hub = component

    @update_graph.register(Connection)
    def _(self, component: Connection):
        self.graph.connections.append(component)


def mainparser() -> None:
    parser = ParserConfig()
    parser.parse_in_type_line()
    print("is ok")
    pass


def maingraph() -> None:
    pass


if __name__ == "__main__":
    mainparser()
    # try:
    # except Exception as error:
    #     if isinstance(error, BaseError):
    #         print(error.get_error())
    #     else:
    #         print(error)
