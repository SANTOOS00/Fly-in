from typing import Protocol, List, Dict, Any
from abc import ABC
from pathlib import Path
import os
import sys
from typing import TextIO
from functools import singledispatchmethod
from custom_error import ErrorSeverity, ErrorLocation, PathError, HubError
from custom_error import ConnectionError, UtilsError, BaseError
from custom_error import ZoneWithCoordsParserError, MetaDataParserError
from utils import Color, COLOR_HEX
import re
# from pydantic import BaseModel, Field
# from typing import Literal, TypedDict


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


class BaseParser(ABC):
    """
    |------------------------------------------------------------------|
    |                  -----    PARSER ARGS   ------                   |
    |------------------------------------------------------------------|
    """
    def __init__(self, line_str: str, line_number: int) -> None:
        self.line_number: int = line_number
        self.line_str: str = line_str


class MetadataValidator:
    def __init__(self,
                 line_number: int,
                 in_type: BaseParser,
                 data: Dict[str, Any]) -> None:
        self.line_number = line_number
        self.in_type = in_type
        self.data = data

    @property
    def get_color(self) -> str:
        return self.data['color']

    @property
    def get_name_zone(self) -> str:
        return self.data['zone']

    @property
    def get_max_drones(self) -> int:
        try:
            return int(self.data['max_drones'])
        except Exception:
            raise MetaDataParserError(
                "Invalid value for 'max_drones' in metadata: "
                f"{self.data['max_drones']}",
                self.line_number,
                ErrorSeverity.Error
            )

    @property
    def get_link_capacity(self) -> int:
        try:
            return int(self.data['max_link_capacity'])
        except Exception:
            raise MetaDataParserError(
                "Invalid value for 'max_drones' in metadata: "
                f"{self.data['max_drones']}",
                self.line_number,
                ErrorSeverity.Error
            )

    @property
    def get_max_capacity(self) -> str:
        return self.data['max_link_capacity']

    def validate_metadata(self) -> Dict[str, Any]:
        self.allowed_status_meta()
        if self.data.get("color"):
            self.data["color"] = self.get_hex(self.get_color)
        if self.data.get("zone"):
            self.data['zone'] = self.allowed_status_zone(self.get_name_zone)
        if self.data.get('max_drones'):
            self.data['max_drones'] = self.get_max_drones
        if self.data.get('max_link_capacity'):
            self.data['max_link_capacity'] = self.get_link_capacity
        return (self.data)

    def get_hex(self, color: str) -> str:
        try:
            c = Color(color.lower())
            return COLOR_HEX[c]
        except ValueError:
            raise UtilsError(
                f"invalid color '{color}'. "
                f"Allowed: {[c.value for c in Color]}",
                self.line_number,
                ErrorSeverity.Error,
            )

    def allowed_status_zone(self, status_zone: str) -> str:
        allowed = ["normal", "blocked", "restricted", "priority"]
        status = status_zone.lower()
        if status not in allowed:
            raise UtilsError(
                f"Invalid status_zone '{status}'. Allowed values: "
                f"{', '.join(allowed)}",
                self.line_number,
                ErrorSeverity.Error,
            )
        return status

    def allowed_status_meta(self) -> None:
        allowed = ["zone", "color", "max_drones"]
        if isinstance(self.in_type, ConnectionParser):
            for key in self.data.keys():
                if key not in "max_link_capacity":
                    raise MetaDataParserError(
                        "Invalid connection metadata\n \n ⚠ Fix: "
                        f"key '{self.data}'"
                        f"allowed \n 'max_link_capacity' just",
                        self.line_number,
                        ErrorSeverity.Error)
        else:
            for key in self.data.keys():
                if key not in allowed:
                    raise MetaDataParserError(
                        "Invalid connection metadata\n \n ⚠ "
                        f"Fix: key '{self.data}'"
                        f"\n           allowed       \n'{allowed}'\n "
                        "           just",
                        self.line_number,
                        ErrorSeverity.Error)


class MetaParser:
    patternsmetadata = {
        r'^\s*\w+=\w+': False,
        r'^\s*\w+=\w+(?:\s+\w+=\w+)*\s*$': False,
    }

    def __init__(self) -> None:
        self.match: re.Match
        self.typ_obj: BaseError

    def parse_metadata(self, meta_data: str) -> Dict[str, str]:
        if len(meta_data) < 4:
            return (self._default_val())
        meta_data = self._validate_metadata_format(meta_data)
        self._check_syntax_meta(meta_data)
        valid_meta = MetadataValidator(self.line_number,
                                       self,
                                       self._split_key_values())
        return (valid_meta.validate_metadata())

    @staticmethod
    def check_duplicates(data: List[str], line_nu: int) -> None:
        seen = set()
        for itm in [k.split("=")[0].strip() for k in data]:
            if itm in seen:
                raise MetaDataParserError(f"Duplicate metadata item '{itm}',"
                                          " The first occurrence will "
                                          "be used.",
                                          line_nu,
                                          ErrorSeverity.Warning
                                          )
            else:
                seen.add(itm)

    def _split_key_values(self) -> Dict[str, str]:
        data: List[str] = self.match.group().split(" ")
        try:
            MetaParser.check_duplicates(data, self.line_number)
        except Exception as error:
            ParserConfig.append_warning(error)
        return (
            {key.lower(): val
                for keyval in data
                for key, val in [keyval.split("=")]}
        )

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
        return (meta_string[1:-1].strip())

    def _check_syntax_meta(self, meta_data) -> None:
        for pattern in MetaParser.patternsmetadata:
            match = re.match(pattern, meta_data)
            if match is None:
                MetaParser.patternsmetadata[pattern] = True
            else:
                MetaParser.patternsmetadata[pattern] = False
        self._validate_syntax_meta()
        self.match = match

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


class Connection(NetworkNode):
    def __init__(self, connection: set, meta) -> None:
        self.connection = connection
        self.meta = meta


class ConnectionParser(MetaParser):
    _patterns = {
        r'^(\w+)': False,
        r'^(\w+)-(\w+)': False,
        r'^(\w+)-(\w+)(.*)': False
    }

    def __init__(self, line_str: str, line_number: int) -> None:
        self.line_str = line_str
        self.line_number = line_number
        self.match: re.Match

    def _check_syntax(self):
        for pattern in ConnectionParser._patterns.keys():
            self.match = re.match(pattern, self.line_str.strip())
            if self.match is None:
                ConnectionParser._patterns[pattern] = True
            else:
                ConnectionParser._patterns[pattern] = False
        self._validate_syntax()

    def _validate_syntax(self) -> None:
        for is_not_valid in ConnectionParser._patterns.values():
            if is_not_valid:
                raise ConnectionError(
                    "Invalid connection syntax. Expected"
                    "format: 'zoneA-zoneB',\n \n"
                    f" > but got:       {self.line_str}.",
                    self.line_number,
                    ErrorSeverity.Error)

    def parser(self) -> Connection:
        self._check_syntax()
        zone_1, zone_2, *meta = self.match.groups()
        if ParserConfig.instance.validate_connection(zone_1, zone_2):
            raise UtilsError(
                f"Duplicate connection detected: {zone_1}-{zone_2}",
                self.line_number,
                ErrorSeverity.Error
            )
        connection: set = {zone_1, zone_2}
        return (
            Connection(
                connection, self.parse_metadata(meta[0])
            )
        )


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
    def parser(self) -> Hub:
        data: Dict[str, Any] = super().parser()
        return Hub(
            data["zone_name"],
            data["x_coordinate"],
            data["y_coordinate"],
            self.parse_metadata(data["metadata"]),
        )


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
                parser_component = self.base_parser(self.clean_line,
                                                    self.number_line)
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
        raise Exception()


class Graph:
    def __init__(self) -> None:
        self.drones: Drones = None
        self.start_hub: Start_hub = None
        self.hubs: List[Hub] = []
        self.end_hub: End_hub = None
        self.connections: List[Connection] = []


class ParserConfig:
    instance = None

    def __init__(self) -> None:
        self.errors: List[str] | None = []
        self.warning: List[str] | None = []
        self.graph = Graph()
        ParserConfig.instance = self

    def has_invalid_zone_names(self, zone_1, zone_2: set) -> bool:
        if zone_1 not in [zone.name for zone in self.graph.hubs]:
            return True
        if zone_2 not in [zone.name for zone in self.graph.hubs]:
            return True
        return False

    def validate_connection(cls, zone_1, zone_2: Connection) -> bool:
        # if cls.instance.has_invalid_zone_names(zone_2, zone_1):
            # return True
        if cls.instance.is_duplicate_connection({zone_2, zone_1}):
            return True
        return False

    def parse_in_type_line(self) -> Graph:
        fileread = SafeFileReader(Path(sys.argv[1]))
        while (True):
            try:
                component = fileread.get_validated_line()
                if component == "EOF":
                    break
                self.update_graph(component)
            except Exception as error:
                self.errors.append(error)
                continue
        self.print_report()
        return (self.graph)

    @property
    def get_graph(self) -> Graph:
        return self.graph

    @staticmethod
    def append_errors(error) -> None:
        ParserConfig.instance.errors.append(error)

    @staticmethod
    def append_warning(error) -> None:
        ParserConfig.instance.warning.append(error)

    def print_report(self) -> None:
        if self.warning:
            string_error = ""
            print(f"\n💥 Found {len(self.warning)} Warning(s) in "
                  "configuration file:", file=sys.stderr)
            for error in self.warning:
                string_error += (f" ⚠️  + {error}\n")
            print(string_error, file=sys.stderr)
        if self.errors:
            string_error = ""
            print(f"\n💥 Found {len(self.errors)} Error(s) in "
                  "configuration file:", file=sys.stderr)
            for error in self.errors:
                string_error += (f" ⚠️  + {error}\n")
            string_error += ("\n❌ Pipeline Status: FAILED\n")
            raise ValueError(string_error)

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

    @property
    def get_conn(self) -> None:
        return (
            [conn.connection for conn in self.graph.connections]
        )

    def is_duplicate_connection(self, component: Connection) -> bool:
        if component in [connection.connection for connection in self.graph.connections]:
            return True

    @staticmethod
    def check_duplicate_zone(name_zone: str) -> bool:
        instan = ParserConfig.instance
        if name_zone in [hub.name for hub in instan.graph.hubs]:
            return True
        return False


def mainparser() -> None:
    parser = ParserConfig()
    graph = parser.parse_in_type_line()
    for hub in graph.connections:
        pass
        # print(hub.connection, hub.meta)


def maingraph() -> None:
    pass


if __name__ == "__main__":
    try:
        mainparser()
    except Exception as error:
        print(error, file=sys.stderr)
    finally:
        if SafeFileReader.fd is not None:
            SafeFileReader.fd.close()
