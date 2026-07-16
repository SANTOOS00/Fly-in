from pathlib import Path
from networknode import Connection, Hub, Start_hub, End_hub, Drones
from typing import List, Dict, Any
import os
import sys
from typing import TextIO
from utils import Color, COLOR_HEX
from functools import singledispatchmethod
from network import FlightNetwork
from custom_error import ErrorLocation, PathError, ErrorSeverity
from custom_error import ConnectionError, UtilsError, BaseError
from custom_error import ZoneWithCoordsParserError, MetaDataParserError
import re


class BaseParser:
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
            val = int(self.data['max_drones'])
            if val < 0:
                raise MetaDataParserError(
                    "Invalid value for 'max_drones' in metadata: "
                    f"{self.data['max_drones']}",
                    self.line_number,
                    ErrorSeverity.Error
                    )
            return val
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
            val = int(self.data['max_link_capacity'])
            if val < 0:
                raise MetaDataParserError(
                    "Invalid value for 'max_link_capacity' in metadata: "
                    f"{self.data['max_link_capacity']}. "
                    "It must be an integer greater than or equal to 1.",
                    self.line_number,
                    ErrorSeverity.Error
                    )
            return val
        except Exception:
            raise MetaDataParserError(
                "Invalid value for 'max_link_capacity' in metadata: "
                f"{self.data['max_link_capacity']}. "
                "It must be an integer greater than or equal to 1.",
                self.line_number,
                ErrorSeverity.Error
            )

    @property
    def _set_color(self) -> None:
        if self.data.get('color'):
            self.data["color"] = self.get_hex(self.get_color)
        else:
            self.data["color"] = self.get_hex('white')

    @property
    def _set_type_zone(self) -> None:
        if self.data.get('zone'):
            self.data['zone'] = self.allowed_status_zone(self.get_name_zone)
        else:
            self.data['zone'] = self.allowed_status_zone('normal')

    @property
    def _set_max_drones(self) -> None:
        if self.data.get('max_drones'):
            self.data['max_drones'] = self.get_max_drones
        else:
            self.data['max_drones'] = 1
    
    @property
    def _set_max_capacity(self) -> None:
        if self.data.get('max_link_capacity'):
            self.data['max_link_capacity'] = self.get_link_capacity

    def validate_metadata(self) -> Dict[str, Any]:
        self.allowed_status_meta()
        self._set_color
        self._set_type_zone
        self._set_max_drones
        self._set_max_capacity
        return (self.data)

    def get_hex(self, color: str) -> str:
        try:
            c = Color(color.lower())
            return COLOR_HEX[c]
        except ValueError:
            return "#FFFFFF"

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
        r'^\s*\w+=[a-zA-Z0-9]+': False,
        r'^\s*\w+=[a-zA-Z0-9]+(\s+\w+=[a-zA-Z0-9]+)?': False,
        r'^\s*\w+=[a-zA-Z0-9]+(\s+\w+=[a-zA-Z0-9]+)?(\s+\w+=[a-zA-Z0-9]+)?$': False,
        r'^\s*\w+=[a-zA-Z0-9]+(\s+\w+=[a-zA-Z0-9]+)*\s*$': False,
    }

    def __init__(self) -> None:
        self.match: re.Match
        self.typ_obj: BaseError

    def parse_metadata(self, meta_data: str) -> Dict[str, str]:
        if len(meta_data) == 0:
            return (self._default_val())
        meta_data = self._validate_metadata_format(meta_data)
        if len(meta_data) == 0:
            return (self._default_val())
        self._check_syntax_meta(meta_data)

        valid_meta = MetadataValidator(self.line_number,
                                       self,
                                       self._split_key_values())
        return (valid_meta.validate_metadata())

    @staticmethod
    def check_duplicates(data: tuple[str], line_nu: int) -> None:
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
        data: str = self.match.group().split()
        try:
            MetaParser.check_duplicates(data, self.line_number)
        except Exception as error:
            ParserConfig.append_warning(error)

        return (
            {key.lower().strip(): val
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
        self._validate_syntax_meta(meta_data.split())
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

    def _validate_syntax_meta(self, data: List[str]) -> None:
        for index, is_not_valid in enumerate(MetaParser.patternsmetadata.
                                             values()):
            if is_not_valid:
                raise MetaDataParserError("Invalid MetaData property syntax at"
                                          f" position {data[index]}. Expected "
                                          "format: ''.",
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
            r'^([^\s-]+)(\s)': False,
            r'^([^\s-]+)\s+(-?\d+)': False,
            r'^([^\s-]+)\s+(-?\d+)\s+(-?\d+)(.*)': False,
        }

    def parser(self) -> Dict[str, Any]:
        self._check_syntax(self.line_str.strip())
        match = re.match(r'^(\w+)\s+(-?\d+)\s+(-?\d+)(.*)',
                         self.line_str.strip())
        name, x, y, *meta = match.groups()
        self.has_invalid_zone_names(name)
        return {
            "zone_name": name,
            "x_coordinate": int(x),
            "y_coordinate": int(y),
            "metadata": meta[0]
        }

    def has_invalid_zone_names(self, zone_name) -> None:
        zones: List[str] = ParserConfig.get_all_zone_names()
        if zone_name in zones:
            raise UtilsError(
                f"Duplicate zone name '{zone_name}' detected. Each "
                "zone name must be unique.",
                self.line_number,
                ErrorSeverity.Error
            )

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


class ConnectionParser(MetaParser):
    _patterns = {
        r'^([^\s-]+)-': False,
        r'^([^\s-]+)-([^\s-]+)': False,
        r'^([^\s-]+)-([^\s-]+)(.*)': False
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
                    "Invalid connection format. Expected "
                    "format: 'zone1-zone2' (no spaces). \n"
                    "\n Zone names may contain any characters except spaces "
                    "and hyphens ('-').\n"
                    f" > but got:       {self.line_str}.",
                    self.line_number,
                    ErrorSeverity.Error)

    def parser(self) -> Connection:
        self._check_syntax()
        zone_1, zone_2, *meta = self.match.groups()
        self.validate_connection(zone_1, zone_2)
        connection: set = {zone_1, zone_2}
        return (
            Connection(
                connection, self.parse_metadata(meta[0])
            )
        )

    def validate_connection(self, zone_1, zone_2: Connection):
        if self.is_duplicate_connection({zone_2, zone_1}):
            raise UtilsError(
                f"Duplicate connection detected: {zone_1}-{zone_2}",
                self.line_number,
                ErrorSeverity.Error
            )
        self.validate_connection_zones(zone_1, zone_2)

    def is_duplicate_connection(self, component: Connection) -> bool:
        connes = ParserConfig.get_connection()
        if component in connes:
            return True
        return False

    def validate_connection_zones(self, source_zone: str,
                                  destination_zone: str) -> None:
        """
        Validate that both zones exist before creating a connection.
        Raises UtilsError if any zone is invalid.
        """
        zones = ParserConfig.get_all_zone_names()
        if source_zone not in zones:
            raise UtilsError(
                f"Invalid source zone: '{source_zone}' does not exist.",
                self.line_number,
                ErrorSeverity.Error
            )

        if destination_zone not in zones:
            raise UtilsError(
                f"Invalid destination zone: '{destination_zone}' "
                "does not exist.",
                self.line_number,
                ErrorSeverity.Error
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


class ParserConfig:
    instance = None

    def __init__(self) -> None:
        self.errors: List[str] | None = []
        self.warning: List[str] | None = []
        self.network = FlightNetwork()
        ParserConfig.instance = self

    def parse_in_type_line(self) -> None:
        fileread = SafeFileReader(Path(sys.argv[1]))
        while (True):
            try:
                component = fileread.get_validated_line()
                if component == "EOF":
                    break
                self.update_network(component)
            except Exception as error:
                self.errors.append(error)
                continue
        self.print_report()
        self.validate_hub_end_start

    @property
    def validate_hub_end_start(self) -> None:
        if self.network.start_hube is None:
            raise ValueError(
                "[Error]: Missing Start Hub! \n  You must define at least "
                "one start hub using this format:\n"
                "    >> start_hub: name_zone x y [key=val] <<"
            )
        if self.network.end_hube is None:
            raise ValueError(
                "[Error]: Missing End Hub! \n  You must define at least "
                "one end hub using this format:\n"
                "     >> start_end: name_zone x y [key=val] <<"
            )

    @property
    def get_network(self) -> FlightNetwork:
        return self.network

    @classmethod
    def append_errors(cls, error) -> None:
        cls.instance.errors.append(error)

    @classmethod
    def append_warning(cls, error) -> None:
        cls.instance.warning.append(error)

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
    def update_network(self, component):
        pass

    @update_network.register(Drones)
    def _(self, component: Drones):
        self.network.drones = component
    
    @update_network.register(Start_hub)
    def _(self, component: Start_hub) -> None:
        self.network.start_hube = component
        self.network.hubs[component.name] = component

    @update_network.register(End_hub)
    def _(self, component: End_hub) -> None:
        self.network.end_hube = component
        self.network.hubs[component.name] = component

    @update_network.register(Hub)
    def _(self, component: Hub | Start_hub | End_hub) -> None:
        self.network.hubs[component.name] = component

    @update_network.register(Connection)
    def _(self, component: Connection):
        self.network.connections.append(component)

    @classmethod
    def get_all_zone_names(cls) -> List[str]:
        network = cls.instance.network
        return list(network.hubs.keys())

    @classmethod
    def get_connection(cls) -> List[set[str, str]]:
        return [con.connection for con in cls.instance.network.connections]
