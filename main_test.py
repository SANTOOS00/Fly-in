from typing import List, Dict, Any
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
import os
import sys
from typing import TextIO
from functools import singledispatchmethod
import re


class ErrorSeverity(Enum):
    Warning = "Warning"
    Error = "Error"


class ErrorLocation(Enum):
    ZONE = "Zone name is not valid"
    X_AXIS = "X coordinate is not valid"
    Y_AXIS = "Y coordinate is not valid"


class BaseError(Exception):
    """
    #|------------------------------------------------------------------|
    #|            ----- custom errors in project ------                 |
    #|------------------------------------------------------------------|
    """

    def __init__(self, message: str, line_number: int | None = None,
                 severity: ErrorSeverity | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.line_number = line_number
        self.severity = severity

    def __str__(self) -> str:
        return (
            f"[{self.severity.value}] line {self.line_number}: "
            f"{self.message}")


class PathError(BaseError):
    def __init__(self, message: str, severity: ErrorSeverity | None = None
                 ) -> None:
        super().__init__(message, severity=severity)

    def __str__(self) -> str:
        return f"[{self.type_error.value}]: {self.message}"


class HubError(BaseError):
    def __init__(self, message: str, line_number: int, severity: ErrorSeverity
                 ) -> None:
        super().__init__(message, line_number, severity)

    def __str__(self):
        return super()._get_error()


class ConnectionError(BaseError):
    def __init__(self, message: str, line_number: int,
                 severity: ErrorSeverity) -> None:
        super().__init__(message, line_number, severity)

    def __str__(self):
        return super()._get_error()


class UtilsError(BaseError):
    def __init__(self, message: str, line_number: int | None = None,
                 severity: ErrorSeverity | None = None) -> None:
        super().__init__(message, line_number, severity)

    def __str___(self):
        return f"{self.message}"


class ZoneWithCoordsParserError(BaseError):
    def __init__(self,
                 message: str,
                 line_number: int | None = None,
                 severity: ErrorSeverity | None = None,
                 location: ErrorLocation | None = None) -> None:
        super().__init__(message, line_number, severity)
        self.location = location

    def __str__(self) -> None:
        if self.location == ErrorLocation.ZONE:
            return (
                f"\n[{self.severity.value}] Line {self.line_number}"
                f" at {self.location.value}:\n"
                f"  ➜ Input Error: {self.message}\n"
                f"  ⚠  Fix: {self.severity.value} ⚠  Fix: Zone format "
                "is invalid. It must be an alphanumeric identifier "
                "(e.g., 's_0').\n"
            )
        else:
            return (
                f"\n[{self.severity.value}] Line {self.line_number}"
                f" at {self.location.value}:\n"
                f"  ➜ Input Error: {self.message}\n"
                f"  ⚠  Fix: {self.severity.value} coordinates must be integers"
                " or negative numbers only.\n"
            )


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


class DroneParser(BaseParser):
    def __init__(self, line_str: str, nu_line: int) -> None:

        super().__init__(line_str, nu_line)

    def parser(self) -> Drones:
        try:
            if int(self.line_str) > 0:
                return Drones(int(self.line_str))
            else:
                raise UtilsError("'nb_drones' value must be a valid integer.",
                                 self.nu_line, ErrorSeverity.Error)
        except ValueError:
            raise UtilsError("'nb_drones' value must be a valid integer.",
                             self.nu_line, ErrorSeverity.Error)


class ZoneWithCoordsParser(BaseParser):
    def __init__(self, line_str: str, nu_line: int) -> None:
        self.line_str = line_str
        self.nu_line = nu_line
        self._patterns = {
            r'^(\w+)': False,
            r'^(\w+)\s+(-?\d+)': False,
            r'^(\w+)\s+(-?\d+)\s+(-?\d+)(\s)(.*)': False,
        }

    def parser(self) -> None:
        line = self.line_str.strip()
        for key in self._patterns.keys():
            match = re.match(key, line)
            if match is None:
                self._patterns[key] = True
        errors = list(ErrorLocation)
        for index, is_not_valid in enumerate(self._patterns.values()):

            if is_not_valid:
                raise ZoneWithCoordsParserError("",
                                                self.nu_line,
                                                ErrorSeverity.Error,
                                                errors[index - 1])


class StartHubParser(ZoneWithCoordsParser):
    def __init__(self, line_str: str, nu_line: int) -> None:
        super().__init__(line_str, nu_line)

    def parser(self) -> Start_hub:
        super().parser()


class EndHubParser(ZoneWithCoordsParser):
    def __init__(self, line_str: str, nu_line: int) -> None:
        super().__init__(line_str, nu_line)

    def parser(self) -> End_hub:
        super().parser()


class HubParser(ZoneWithCoordsParser):
    def __init__(self, line_str: str, nu_line: int) -> None:
        super().__init__(line_str, nu_line)

    def parser(self) -> Hub:
        super().parser()


class ConnectionParser:
    def __init__(self, line_str: str, nu_line: int) -> None:
        self.line_str = line_str
        self.nu_line = nu_line

    def parser(self) -> Connection:
        pass


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
                f"File not found: {path_file}", ErrorSeverity.Error)
        if not os.access(path_file, os.R_OK):
            raise PathError(
                f"No read permission: {path_file}", ErrorSeverity.Error)
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
                    self.number_line, ErrorSeverity.Error)

    def __del__(self) -> None:
        self._fd.close()

    def _get_type_line(self) -> bool:
        if self.data_str.count(":") != 1:
            raise UtilsError(
                "The line type must match one of the allowed formats "
                "{nb_drones, start_hub, etc.}. Example: [type: ,,, ]",
                self.number_line, ErrorSeverity.Error)
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
                    break
            except Exception as error:
                self.errors.append(error)
            self.update_graph(component)
        self.print_report()

    def print_report(self) -> None:

        if self.errors:
            string_error = ""
            print(f"\n💥 Found {len(self.errors)} Error(s) in "
                  "configuration file:", file=sys.stderr)
            for error in self.errors:
                string_error += (f" ⚠️  + {error}\n")
            string_error += ("\n❌ Pipeline Status: FAILED\n")
            raise Exception(string_error)

    @singledispatchmethod
    def update_graph(self, data):
        pass

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


def maingraph() -> None:
    pass


if __name__ == "__main__":
    try:
        mainparser()
    except Exception as error:
        print(error, file=sys.stderr)
