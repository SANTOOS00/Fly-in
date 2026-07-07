from typing import Protocol, List, Dict, Any
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
import os
import sys
from typing import TextIO
from functools import singledispatchmethod
from typing import Literal, TypedDict
from custom_error import *
# from pydantic import BaseModel, Field
import re


class NetworkNode(Protocol):
    ...


class Drones(NetworkNode):
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


class End_hub(NetworkNode):
    _number_line_start = None
    _instance: "End_hub" = None

    def __new__(cls, name: str, y: int, x: int,
                meta: Dict[str, Any] | None = None,
                line_number: int | None = None) -> "End_hub":
        if cls._instance is not None:
            raise HubError(
                "Duplicate End hub at lines "
                f"{cls._instance._number_line_start} "
                f"and {line_number}. Only one is allowed.",
                line_number,
                ErrorSeverity.Error)

        cls._instance = super().__new__(cls)
        cls._number_line_start = line_number
        cls._instance.name = name
        cls._instance.y = y
        cls._instance.x = x
        cls._instance.meta = meta
        return cls._instance


class Start_hub(NetworkNode):
    _number_line_start = None
    _instance: "Start_hub" = None

    def __new__(cls, name: str, y: int, x: int,
                meta: Dict[str, Any] | None = None,
                line_number: int | None = None) -> "Start_hub":
        if cls._instance is not None:
            raise HubError(
                "Duplicate Start hub at lines "
                f"{cls._instance._number_line_start} "
                f"and {line_number}. Only one is allowed.",
                line_number,
                ErrorSeverity.Error)
        else:
            cls._instance = super().__new__(cls)

        Start_hub._number_line_start = line_number
        cls._instance = super().__new__(cls)
        cls._instance.name = name
        cls._instance.y = y
        cls._instance.x = x
        cls._instance.meta = meta
        return cls._instance


class Hub(NetworkNode):
    def __init__(self, name: str, y: int, x: int,
                 meta: Dict[str, Any] | None = None
                 ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.meta: Dict[str: Any] | None = meta


class Connection(NetworkNode):
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
    def __init__(self, line_str: str, line_number: int) -> None:
        self.line_number: int = line_number
        self.line_str: str = line_str


# class start_metadata_hubs(BaseModel):
#     zono = Literal[""]
#     color = Literal[""]
#     age: int = Field(ge=1, le=sys.maxsize)


class MetaParser:
    patternsmetadata = {
        r'^\s*\w+=\w+': False,
        r'^\s*\w+=\w+(?:\s+\w+=\w+)*\s*$': False,
    }

    def parse_metadata(self, meta_data: str) -> Dict[str, str]:
        if len(meta_data) <= 3 or meta_data == "[]":
            return (self._default_val())
        meta_data = self._validate_metadata_format(meta_data)
        match = self._check_syntax_meta(meta_data)
        return (self._check_data_is_valid(match))

    @staticmethod
    def _split_key_values(match: re.Match[str]) -> dict[str, str]:
        data: set = match.group().split(" ")
        MetaParser._check_data_is_valid()
        return (
            {key: val
                for keyval in data
                for key, val in [keyval.split("=")]}
        )

    @staticmethod
    def _check_data_is_valid(data: Dict[str, str]) -> Dict[str, Any]:
        

    def _validate_metadata_format(self, meta_data: str) -> str:
        meta_string = meta_data.strip()
        if not meta_string.startswith("["):
            raise MetaDataParserError("MetaData must start with '['",
                                      self.line_number,
                                      ErrorSeverity.Error)
        if not meta_string.endswith("]"):
            raise MetaDataParserError("MetaData missing closing bracket ']'",
                                      self.line_number,
                                      ErrorSeverity.Error)
        return (meta_string[1:-1])

    def _check_syntax_meta(self, meta_data) -> None:
        for pattern in MetaParser.patternsmetadata:
            match = re.match(pattern, meta_data)
            if match is None:
                MetaParser.patternsmetadata[pattern] = True
            else:
                MetaParser.patternsmetadata[pattern] = False
        self._validate_syntax_meta()
        return (match)

    def _default_val(self) -> dict[str, int]:
        if isinstance(self, ConnectionParser):
            return {
                "max_link_capacity": 1
            }
        else:
            return {
                "max_drones": 1
            }

    def _validate_syntax_meta(self) -> None:
        for index, is_not_valid in enumerate(MetaParser.patternsmetadata.
                                             values()):
            if is_not_valid:
                raise MetaDataParserError("Invalid MetaData property syntax at"
                                          f" position {index + 1}. Expected "
                                          "format: 'key=value'.",
                                          self.line_number,
                                          ErrorSeverity.Error,
                                          )


class DroneParser(BaseParser):
    def parser(self) -> Drones:
        try:
            if int(self.line_str) > 0:
                return Drones(int(self.line_str))
            else:
                raise UtilsError("'nb_drones' value must be a valid integer.",
                                 self.line_number, ErrorSeverity.Error)
        except ValueError:
            raise UtilsError("'nb_drones' value must be a valid integer.",
                             self.line_number, ErrorSeverity.Error)


class ZoneWithCoordsParser(BaseParser):
    patterns = {
            r'^(\w+)(\s)': False,
            r'^(\w+)\s+(-?\d+)': False,
            r'^(\w+)\s+(-?\d+)\s+(-?\d+)(.*)': False,
        }

    def parser(self) -> Dict[str, Any]:
        self._check_syntax(self.line_str.strip())
        match = re.match(r'^(\w+)\s+(-?\d+)\s+(-?\d+)(.*)',
                         self.line_str.strip())
        name, x, y, *meta = match.groups()
        return {
            "zone_name": name,
            "x_coordinate": int(x),
            "y_coordinate": int(y),
            "metadata": meta[0]
        }

    def _check_syntax(self, line: str) -> None:
        line = self.line_str.strip()
        for pattern in ZoneWithCoordsParser.patterns.keys():
            match = re.match(pattern, line)
            if match is None:
                ZoneWithCoordsParser.patterns[pattern] = True
            else:
                ZoneWithCoordsParser.patterns[pattern] = False
        self._validate_syntax()

    def _validate_syntax(self) -> None:
        errors = list(ErrorLocation)
        for index, is_not_valid in enumerate(ZoneWithCoordsParser.patterns.
                                             values()):
            if is_not_valid:
                raise ZoneWithCoordsParserError("",
                                                self.line_number,
                                                ErrorSeverity.Error,
                                                errors[index])


class StartHubParser(ZoneWithCoordsParser, MetaParser):
    def parser(self) -> Start_hub:
        data: Dict[str, Any] = super().parser()
        return Start_hub(
            data["zone_name"],
            data["x_coordinate"],
            data["y_coordinate"],
            self.parse_metadata(data["metadata"]),
            self.line_number
        )


class EndHubParser(ZoneWithCoordsParser, MetaParser):
    def __init__(self, line_str: str, line_number: int) -> None:
        super().__init__(line_str, line_number)

    def parser(self) -> End_hub:
        data: Dict[str, Any] = super().parser()
        return End_hub(
            data["zone_name"],
            data["x_coordinate"],
            data["y_coordinate"],
            self.parse_metadata(data["metadata"]),
            self.line_number
        )


class HubParser(ZoneWithCoordsParser, MetaParser):
    def __init__(self, line_str: str, line_number: int) -> None:
        super().__init__(line_str, line_number)

    def parser(self) -> Hub:
        data: Dict[str, Any] = super().parser()
        return Hub(
            data["zone_name"],
            data["x_coordinate"],
            data["y_coordinate"],
            self.parse_metadata(data["metadata"]),
        )


class ConnectionParser:
    def __init__(self, line_str: str, line_number: int) -> None:
        self.line_str = line_str
        self.line_number = line_number

    def parser(cls) -> Connection:
        return (None)


class SafeFileReader:
    fd: TextIO = None

    def __init__(self, path_file: Path) -> None:
        self.valid_path: Path = path_file
        self.number_line: int = 0
        self.base_parser: BaseParser
        self.clean_line: str
        self.raw_line: str

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
        SafeFileReader.fd: TextIO = open(path_file, encoding="utf-8")

    def get_validated_line(self) -> Dict[str, str] | str:
        while True:
            raw_line = SafeFileReader.fd.readline()
            if not raw_line:
                return "EOF"
            self.number_line += 1
            self.data_str = raw_line.split("#", maxsplit=1)[0].strip()
            if self.data_str == "":
                continue
            if self._get_type_line():
                parser_component = self.base_parser(self.clean_line, self.number_line)
                return (parser_component.parser())
            else:
                raise UtilsError(
                    f"Unknown configuration token '{self.raw_line}'",
                    self.number_line, ErrorSeverity.Error)

    def _get_type_line(self) -> bool:
        if self.data_str.count(":") != 1:
            raise UtilsError(
                "The line type must match one of the allowed formats "
                "{nb_drones, start_hub, etc.}. Example: [type: ,,, ]",
                self.number_line, ErrorSeverity.Error)
        key_raw, self.clean_line = self.data_str.split(":", 1)
        self.base_parser = key_raw.lower()
        parsers = {
            "nb_drones": DroneParser,
            "start_hub": StartHubParser,
            "hub": HubParser,
            "end_hub": EndHubParser,
            "connection": ConnectionParser
        }
        if parsers.get(self.base_parser):
            self.base_parser = parsers[self.base_parser]
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

    def parse_in_type_line(self) -> Graph:
        fileread = SafeFileReader(Path(sys.argv[1]))
        while (True):
            # try:
            component = fileread.get_validated_line()
            if component == "EOF":
                break
            # except Exception as error:
            #     self.errors.append(error)
                continue
            self.update_graph(component)
        self.print_report()
        return (self.graph)

    @property
    def get_graph(self) -> Graph:
        return self.graph

    def print_report(self) -> None:
        if self.errors:
            string_error = ""
            print(f"\n💥 Found {len(self.errors)} Error(s) in "
                  "configuration file:", file=sys.stderr)
            for error in self.errors:
                string_error += (f" ⚠️  + {error}\n")
            string_error += ("\n❌ Pipeline Status: FAILED\n")
            raise Exception(string_error)
        SafeFileReader.fd.close()

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
    graph = parser.parse_in_type_line()
    for hub in graph.hubs:
        print(hub.)

def maingraph() -> None:
    pass


if __name__ == "__main__":
    try:
        mainparser()
    except Exception as error:
        print(error, file=sys.stderr)
