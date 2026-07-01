from typing import List, Dict, Any, Tuple, Optional
from abc import ABC, abstractmethod
from start_hub import Start_hub
from end_hub import End_hub
from connection import Connection
from hub import Hub
from drones import Drones
from custom_error import ParsingError
from utils import Utils
from graph import Graph
from functools import singledispatch

import sys


@singledispatch
def append() -> None:
    pass


class BaseParser(ABC):
    def __init__(self, raw_line: str, line_number: int) -> None:
        self.raw_line = raw_line
        self.line_number = line_number

    @abstractmethod
    def parse(self) -> Any:
        pass

    def parse_metadata(self, meta_string: str) -> Dict[str, str]:
        meta_string = meta_string.strip()
        if not meta_string.startswith("["):
            raise ParsingError("MetaData must start with '['")
        if not meta_string.endswith("]"):
            raise ParsingError("MetaData missing closing bracket ']'")
        content = meta_string[1:-1].strip()
        result_dict = {}
        if not content:
            return result_dict
        pairs = content.split()
        for pair in pairs:
            if "=" not in pair:
                raise ParsingError(
                    f"Invalid MetaData property '{pair}'"
                    ". Expected 'key=value'")
            key, value = pair.split("=", 1)
            key = key.strip()
            value = value.strip()
            if not key or not value:
                raise ParsingError(
                    f"MetaData key or value cannot be empty in '{pair}'")
            if key in result_dict:
                raise ParsingError(
                    f"Duplicate MetaData key '{key}' found. "
                    f"Each property can only be defined once."
                )
            result_dict[key] = value
        return result_dict


class DroneParser(BaseParser):
    def parse(self) -> Drones:
        try:
            return Drones(int(self.raw_line))
        except ValueError:
            raise ParsingError(f"'nb_drones' value '{self.raw_line}' "
                               f"must be a valid integer.")

    @append.register(Drones)
    def _(data, graph: Graph) -> None:
        graph.drones = data


class NodeParser(BaseParser):
    def split_line(self) -> Tuple[str, int, int, Optional[str]]:
        data = self.raw_line.split(" ", 3)
        if len(data) < 3:
            raise ParsingError(
                "Invalid format. Expected 'name Y X [metadata]'")
        name = data[0].strip()
        try:
            y = int(data[1])
        except ValueError:
            raise ParsingError(f"Y coordinate '{data[1]}' must be an integer.")
        try:
            x = int(data[2])
        except ValueError:
            raise ParsingError(f"X coordinate '{data[2]}' must be an integer.")
        meta_str = data[3].strip() if len(data) == 4 else None
        return name, y, x, meta_str

    def validate_common_meta(self, meta_dict: Dict[str, Any]
                             ) -> Dict[str, Any]:
        if "max_drones" in meta_dict:
            try:
                meta_dict["max_drones"] = int(meta_dict["max_drones"])
            except ValueError:
                raise ParsingError("'max_drones' value must be an integer.")
        if "color" in meta_dict:
            meta_dict["color"] = Utils.get_hex(meta_dict["color"])
        return meta_dict


class StartHubParser(NodeParser):
    def parse(self) -> Start_hub:
        name, y, x, meta_str = self.split_line()
        meta_dict = self.parse_metadata(meta_str) if meta_str else {}
        meta_dict = self.validate_common_meta(meta_dict)
        for k in meta_dict:
            if k not in ["color", "max_drones"]:
                raise ParsingError(f"Invalid key '{k}' for start_hub.")
        return Start_hub(name, y, x, meta_dict)

    @append.register(Start_hub)
    def _(data, graph: Graph) -> None:
        graph.start_hub = data


class HubParser(NodeParser):
    def parse(self) -> Hub:
        name, y, x, meta_str = self.split_line()
        meta_dict = self.parse_metadata(meta_str) if meta_str else {}
        meta_dict = self.validate_common_meta(meta_dict)
        if "zone" in meta_dict:
            meta_dict["zone"] = (meta_dict["zone"])
        for k in meta_dict:
            if k not in ["color", "max_drones", "zone"]:
                raise ParsingError(f"Invalid key '{k}' for hub.")
        return Hub(name, y, x, meta_dict)

    @append.register(Hub)
    def _(data, graph: Graph) -> None:
        graph.hubs  .append(data)


class EndHubParser(NodeParser):
    def parse(self) -> End_hub:
        name, y, x, meta_str = self.split_line()
        meta_dict = self.parse_metadata(meta_str) if meta_str else {}
        meta_dict = self.validate_common_meta(meta_dict)
        for k in meta_dict:
            if k not in ["color", "max_drones"]:
                raise ParsingError(f"Invalid key '{k}' for end_hub.")
        return End_hub(name, y, x, meta_dict)

    @append.register(End_hub)
    def _(data, graph: Graph) -> None:
        graph.end_hub = data


class ConnectionParser(BaseParser):
    def parse(self) -> Connection:
        parts = self.raw_line.split(maxsplit=1)
        if not parts:
            raise ParsingError("Empty connection details.")
        link_part = parts[0]
        if "-" not in link_part:
            raise ParsingError("Connection must follow 'node1-node2' format.")
        node1, node2 = link_part.split("-", 1)
        if not node1.strip() or not node2.strip():
            raise ParsingError(
                "Connection nodes cannot be empty."
                )
        meta_dict = {}
        if len(parts) == 2:
            meta_dict = self.parse_metadata(parts[1])
            if "max_link_capacity" in meta_dict:
                try:
                    meta_dict["max_link_capacity"] = int(
                                meta_dict["max_link_capacity"]
                                )
                except ValueError:
                    raise ParsingError(
                        "'max_link_capacity' must be an integer."
                        )
            for k in meta_dict:
                if k != "max_link_capacity":
                    raise ParsingError(
                        f"Invalid connection metadata key '{k}'."
                        )
        return Connection(node1.strip(), node2.strip(), meta_dict)

    @append.register(Connection)
    def _(data, graph: Graph) -> None:
        graph.connections.append(data)


class LineValidator:
    def __init__(self, name_file: str) -> None:
        self.fd = open(name_file, "r")
        self.line_number = 0
        self.error_string: str = None

    def next_parser(self
                    ) -> Tuple[Optional[BaseParser] | str, Optional[str]]:
        line = self.fd.readline()
        self.line_number += 1
        if not line:
            self.fd.close()
            return None, "EOF"
        clean_line = line.strip()
        if not clean_line or clean_line.startswith("#"):
            return None, "COMMENT_OR_EMPTY"
        if ":" not in clean_line:
            raise ParsingError(
                "Syntax error. Expected 'key: value' structure.")
        key, value = clean_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        parsers = {
            "nb_drones": DroneParser,
            "start_hub": StartHubParser,
            "hub": HubParser,
            "end_hub": EndHubParser,
            "connection": ConnectionParser
        }
        if key in parsers:
            return parsers[key](value, self.line_number), "SUCCESS"
        else:
            raise ParsingError(
                f"Unknown configuration token '{key}'")


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
            raise ParsingError(
                "Duplicate 'end_hub' defined. Only one start hub is allowed.")

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
            raise ParsingError(
                "Duplicate 'start_hub' defined. Only "
                "one start hub is allowed.")

        cls._instance = super().__new__(cls)
        cls._instance.name = name
        cls._instance.y = y
        cls._instance.x = x
        cls._instance.meta = meta
        return cls._instance







#|------------------------------------------------------------------|
#|                  -----    PARSER ARGS   ------                   |
#|------------------------------------------------------------------|
class BaseParser(ABC):
    def __init__(self, line_str: str) -> None:
        self.number_line: int = 0
        self.line_str: str = line_str
        self.

    def parser() -> None:
        pass

    @singledispatch
    def append(self, data: ) -> None:
        pass

    @append.register(Hub)
    def _(self, test_name) -> None:

    @append.register(Start_hub)
    def _(self, test_name) -> None:
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
    def __init__(self) -> None:
        self.graph = Graph()
        self.errors: List = list()

    def print_report(self) -> bool:
        if self.errors:
            string_error = ""
            print(f"\n💥 Found {len(self.errors)} Error(s) in "
                  "configuration file:", file=sys.stderr)
            for error in self.errors:
                string_error += (f" ⚠️  + {error}\n")
            string_error += ("\n❌ Pipeline Status: FAILED\n")
            raise ParsingError(string_error)
        return (self.graph)

    def parse_pipeline(self, name_file: str) -> bool:
        validator = LineValidator(name_file)
        while True:
            try:
                parser, status = validator.next_parser()
                if status == "EOF":
                    break
                if status == "COMMENT_OR_EMPTY" or not parser:
                    continue
                if status == "ERROR":
                    continue
                result = parser.parse()
                append(result, self.graph)
            except (ParsingError, ValueError) as err:
                self.errors.append(f"Line {validator.line_number}"
                                   ": " + str(err))
        self.validate_structural_rules()
        return self.print_report()

    def validate_structural_rules(self) -> None:
        if self.graph.drones is None:
            self.errors.append("Global Error: Missing 'nb_drones' "
                               "definition in the file.")
        if self.graph.start_hub is None:
            self.errors.append("Global Error: Missing 'start_hub' definition. "
                               "The simulation needs a starting point.")
        if self.graph.end_hub is None:
            self.errors.append(
                "Global Error: Missing 'end_hub' definition. "
                "The simulation needs a destination point (goal).")

def main() -> None:
    pass

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)