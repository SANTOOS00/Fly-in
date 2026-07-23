
from pathlib import Path
from parser_data import BaseParser, HubParser, EdgeParser, FlyinError
from map import Map
from hube import Hub
from edge import Edge
import os
import sys

class SafeFileReader:
    def __init__(self, path_file: str):
        self.path_file = Path(path_file)

    def _valid_arg(self):
        if len(sys.argv) != 2:
            raise FlyinError(
                "Usage: python main.py <file.txt>"
            )

    def valid_path(self):
        self._valid_arg()

        if not self.path_file.exists():
            raise FlyinError(f"File not found: {self.path_file}")

        if not os.access(self.path_file, os.R_OK):
            raise FlyinError(
                f"No read permission: {self.path_file}"
            )

class Parseline:
    
    def __init__(self) -> None:
        self.raw_line: str
        self.type_line: str
        self.clean_line: str
        self.map = Map()

    def parse_file(self) -> None:
        safe_file = SafeFileReader(sys.argv[1])
        safe_file.valid_path()
        with open(safe_file.path_file, "r") as fb:
            for raw_line in fb:
                self._process_line(raw_line)
    
    def _process_line(self, raw_line: str):
        FlyinError.add_line_number()
        self.raw_line = raw_line.split("#", maxsplit=1)[0].strip()
        if not self.raw_line:
            return
        self._set_type_line()
        self._dispatch_line()
  
    def _dispatch_line(self):
        match self.type_line.upper():
            case "NB_DRONES":
                self._create_number_drones()
            case "START_HUB":
                self._create_start_hube()
            case "HUB":
                self._create_hube()
            case "END_HUB":
                self._create_end_hube()
            case "CONNECTION":
                self._create_edge()

    def _create_start_hube(self) -> None:
        hub: Hub = HubParser(self.clean_line.strip()).parser()
        self.map.set_start_hub(hub)

    def _create_hube(self) -> None:
        hub: Hub = HubParser(self.clean_line.strip()).parser()
        self.map.add_hub(hub)

    def _create_end_hube(self) -> None:
        hub: Hub = HubParser(self.clean_line.strip()).parser()
        self.map.set_end_hub(hub)

    def _create_edge(self) -> None:
        edge: Edge = EdgeParser(self.clean_line.strip()).parser()
        self.map.add_egde(edge)

    def _create_number_drones(self) -> None:
        try:
            self.map.set_number_drones(int(self.clean_line))
        except ValueError:
            raise FlyinError("val li kaukon f drones hwa wahd number sahih tabi3i",
                             line_number=FlyinError.get_number_line())

    def _set_type_line(self) -> None:
        if self.raw_line.count(":") < 0:
            raise FlyinError(
                "The line type must match one of the allowed formats "
                "{nb_drones, start_hub, etc.}. Example: [type: ,,, ]",
                line_numer=FlyinError.get_number_line())
        key_raw, self.clean_line = self.raw_line.split(":", 1)
        parsers = {
            "nb_drones": 'DroneParser',
            "start_hub": HubParser,
            "hub": HubParser,
            "end_hub": HubParser,
            "connection": EdgeParser
        }
        if parsers.get(key_raw.lower()):
            self.type_line = key_raw.lower()
        else:
            raise FlyinError('type error',
                             line_number=FlyinError.get_number_line())



    # def parse_in_type_line(self) -> None:
    #     fileread = SafeFileReader(Path(sys.argv[1]))
    #     while (True):
    #         try:
    #             component = fileread.get_validated_line()
    #             if component == "EOF":
    #                 break
    #             self.update_network(component)
    #         except Exception as error:
    #             self.errors.append(error)
    #             continue
    #     self.print_report()
    
    #         while True:
#             raw_line = SafeFileReader.fd.readline()
#             if not raw_line:
#                 return "EOF"
#             self.number_line += 1
#             self.data_str = raw_line.split("#", maxsplit=1)[0].strip()
#             if self.data_str == "":
#                 continue
#             if self._get_type_line():
#                 parser_component = self.base_parser(self.clean_line,
#                                                     self.number_line)
#                 return (parser_component.parser())
#             else:
#                 raise UtilsError(
#                     f"Unknown configuration token '{self.raw_line}'",
#                     self.number_line, ErrorSeverity.Error)

#     def _get_type_line(self) -> bool:
#         if self.data_str.count(":") != 1:
#             raise UtilsError(
#                 "The line type must match one of the allowed formats "
#                 "{nb_drones, start_hub, etc.}. Example: [type: ,,, ]",
#                 self.number_line, ErrorSeverity.Error)
#         key_raw, self.clean_line = self.data_str.split(":", 1)
#         self.base_parser = key_raw.lower()
#         parsers = {
#             "nb_drones": DroneParser,
#             "start_hub": StartHubParser,
#             "hub": HubParser,
#             "end_hub": EndHubParser,
#             "connection": ConnectionParser
#         }
#         if parsers.get(self.base_parser):
#             self.base_parser = parsers[self.base_parser]
#             return True
#         raise Exception()


#     @property
#     def validate_hub_end_start(self) -> None:
#         if self.network.start_hube is None:
#             raise ValueError(
#                 "[Error]: Missing Start Hub! \n  You must define at least "
#                 "one start hub using this format:\n"
#                 "    >> start_hub: name_zone x y [key=val] <<"
#             )
#         if self.network.end_hube is None:
#             raise ValueError(
#                 "[Error]: Missing End Hub! \n  You must define at least "
#                 "one end hub using this format:\n"
#                 "     >> start_end: name_zone x y [key=val] <<"
#             )


# from networknode import Connection, Hub, Start_hub, End_hub, Drones
# from typing import List, Dict, Any
# import os
# import sys
# from typing import TextIO
# from utils import Color, COLOR_HEX
# from functools import singledispatchmethod
# from network import FlightNetwork
# from custom_error import ErrorLocation, PathError, ErrorSeverity
# from custom_error import ConnectionError, UtilsError, BaseError
# from custom_error import ZoneWithCoordsParserError, MetaDataParserError
# from enums import Type_zone
# import re


# class BaseParser:
#     def __init__(self, line_str: str, line_number: int) -> None:
#         self.line_number: int = line_number
#         self.line_str: str = line_str



# class DroneParser(BaseParser):
#     def parser(self) -> Drones:
#         try:
#             if int(self.line_str) > 0:
#                 return Drones(int(self.line_str))
#             else:
#                 raise UtilsError("'nb_drones' value must be a valid integer.",
#                                  self.line_number, ErrorSeverity.Error)
#         except ValueError:
#             raise UtilsError("'nb_drones' value must be a valid integer.",
#                              self.line_number, ErrorSeverity.Error)


# class ConnectionParser(MetaParser):
#     _patterns = {
#         r'^([^\s-]+)-': False,
#         r'^([^\s-]+)-([^\s-]+)': False,
#         r'^([^\s-]+)-([^\s-]+)(.*)': False
#     }

#     def __init__(self, line_str: str, line_number: int) -> None:
#         self.line_str = line_str
#         self.line_number = line_number
#         self.match: re.Match

#     def _check_syntax(self):
#         for pattern in ConnectionParser._patterns.keys():
#             self.match = re.match(pattern, self.line_str.strip())
#             if self.match is None:
#                 ConnectionParser._patterns[pattern] = True
#             else:
#                 ConnectionParser._patterns[pattern] = False
#         self._validate_syntax()



#     def validate_connection(self, zone_1, zone_2: Connection):
#         if self.is_duplicate_connection({zone_2, zone_1}):
#             raise UtilsError(
#                 f"Duplicate connection detected: {zone_1}-{zone_2}",
#                 self.line_number,
#                 ErrorSeverity.Error
#             )
#         self.validate_connection_zones(zone_1, zone_2)

#     def is_duplicate_connection(self, component: Connection) -> bool:
#         connes = ParserConfig.get_connection()
#         if component in connes:
#             return True
#         return False

#     def validate_connection_zones(self, source_zone: str,
#                                   destination_zone: str) -> None:
#         """
#         Validate that both zones exist before creating a connection.
#         Raises UtilsError if any zone is invalid.
#         """
#         zones = ParserConfig.get_all_zone_names()
#         if source_zone not in zones:
#             raise UtilsError(
#                 f"Invalid source zone: '{source_zone}' does not exist.",
#                 self.line_number,
#                 ErrorSeverity.Error
#             )

#         if destination_zone not in zones:
#             raise UtilsError(
#                 f"Invalid destination zone: '{destination_zone}' "
#                 "does not exist.",
#                 self.line_number,
#                 ErrorSeverity.Error
#             )



# class SafeFileReader:
#     fd: TextIO = None

#     def __init__(self, path_file: Path) -> None:
#         self.valid_path: Path = path_file
#         self.number_line: int = 0
#         self.base_parser: BaseParser
#         self.clean_line: str
#         self.raw_line: str

#     @property
#     def valid_path(self) -> Path:
#         return self._fd

#     @valid_path.setter
#     def valid_path(self, path_file: Path) -> None:
#         if not path_file.exists():
#             raise PathError(
#                 f"File not found: {path_file}", ErrorSeverity.Error)
#         if not os.access(path_file, os.R_OK):
#             raise PathError(
#                 f"No read permission: {path_file}", ErrorSeverity.Error)
#         SafeFileReader.fd: TextIO = open(path_file, encoding="utf-8")

#     def get_validated_line(self) -> Dict[str, str] | str:
#         while True:
#             raw_line = SafeFileReader.fd.readline()
#             if not raw_line:
#                 return "EOF"
#             self.number_line += 1
#             self.data_str = raw_line.split("#", maxsplit=1)[0].strip()
#             if self.data_str == "":
#                 continue
#             if self._get_type_line():
#                 parser_component = self.base_parser(self.clean_line,
#                                                     self.number_line)
#                 return (parser_component.parser())
#             else:
#                 raise UtilsError(
#                     f"Unknown configuration token '{self.raw_line}'",
#                     self.number_line, ErrorSeverity.Error)

#     def _get_type_line(self) -> bool:
#         if self.data_str.count(":") != 1:
#             raise UtilsError(
#                 "The line type must match one of the allowed formats "
#                 "{nb_drones, start_hub, etc.}. Example: [type: ,,, ]",
#                 self.number_line, ErrorSeverity.Error)
#         key_raw, self.clean_line = self.data_str.split(":", 1)
#         self.base_parser = key_raw.lower()
#         parsers = {
#             "nb_drones": DroneParser,
#             "start_hub": StartHubParser,
#             "hub": HubParser,
#             "end_hub": EndHubParser,
#             "connection": ConnectionParser
#         }
#         if parsers.get(self.base_parser):
#             self.base_parser = parsers[self.base_parser]
#             return True
#         raise Exception()


# class ParserConfig:
#     instance = None

#     def __init__(self) -> None:
#         self.errors: List[str] | None = []
#         self.warning: List[str] | None = []
#         self.network = FlightNetwork()
#         ParserConfig.instance = self

#     def parse_in_type_line(self) -> None:
#         fileread = SafeFileReader(Path(sys.argv[1]))
#         while (True):
#             try:
#                 component = fileread.get_validated_line()
#                 if component == "EOF":
#                     break
#                 self.update_network(component)
#             except Exception as error:
#                 self.errors.append(error)
#                 continue
#         self.print_report()
#         self.validate_hub_end_start

#     @property
#     def validate_hub_end_start(self) -> None:
#         if self.network.start_hube is None:
#             raise ValueError(
#                 "[Error]: Missing Start Hub! \n  You must define at least "
#                 "one start hub using this format:\n"
#                 "    >> start_hub: name_zone x y [key=val] <<"
#             )
#         if self.network.end_hube is None:
#             raise ValueError(
#                 "[Error]: Missing End Hub! \n  You must define at least "
#                 "one end hub using this format:\n"
#                 "     >> start_end: name_zone x y [key=val] <<"
#             )

#     @property
#     def get_network(self) -> FlightNetwork:
#         return self.network

#     @classmethod
#     def append_errors(cls, error) -> None:
#         cls.instance.errors.append(error)

#     @classmethod
#     def append_warning(cls, error) -> None:
#         cls.instance.warning.append(error)

#     def print_report(self) -> None:
#         if self.warning:
#             string_error = ""
#             print(f"\n💥 Found {len(self.warning)} Warning(s) in "
#                   "configuration file:", file=sys.stderr)
#             for error in self.warning:
#                 string_error += (f" ⚠️  + {error}\n")
#             print(string_error, file=sys.stderr)
#         if self.errors:
#             string_error = ""
#             print(f"\n💥 Found {len(self.errors)} Error(s) in "
#                   "configuration file:", file=sys.stderr)
#             for error in self.errors:
#                 string_error += (f" ⚠️  + {error}\n")
#             string_error += ("\n❌ Pipeline Status: FAILED\n")
#             raise ValueError(string_error)

#     @singledispatchmethod
#     def update_network(self, component):
#         pass

#     @update_network.register(Drones)
#     def _(self, component: Drones):
#         self.network.drones = component
    
#     @update_network.register(Start_hub)
#     def _(self, component: Start_hub) -> None:
#         self.network.start_hube = component
#         self.network.hubs[component.name] = component

#     @update_network.register(End_hub)
#     def _(self, component: End_hub) -> None:
#         self.network.end_hube = component
#         self.network.hubs[component.name] = component

#     @update_network.register(Hub)
#     def _(self, component: Hub | Start_hub | End_hub) -> None:
#         self.network.hubs[component.name] = component


#     @update_network.register(Connection)
#     def _(self, component: Connection):
#         self.network.connections.append(component)

#     @classmethod
#     def get_all_zone_names(cls) -> List[str]:
#         network = cls.instance.network
#         return list(network.hubs.keys())

#     @classmethod
#     def get_connection(cls) -> List[set[str, str]]:
#         return [con.connection for con in cls.instance.network.connections]
