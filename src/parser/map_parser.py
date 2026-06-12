from typing import List, Dict, Any, Tuple, Optional
from abc import ABC, abstractmethod
from simulation import Start_hub, Hub, End_hub, Drones, Connection
from .custom_error import ParsingError
from utils import get_hex, allowed_status
import sys


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
            meta_dict["color"] = get_hex(meta_dict["color"])
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


class HubParser(NodeParser):
    def parse(self) -> Hub:
        name, y, x, meta_str = self.split_line()
        meta_dict = self.parse_metadata(meta_str) if meta_str else {}
        meta_dict = self.validate_common_meta(meta_dict)
        if "zone" in meta_dict:
            meta_dict["zone"] = allowed_status(meta_dict["zone"])
        for k in meta_dict:
            if k not in ["color", "max_drones", "zone"]:
                raise ParsingError(f"Invalid key '{k}' for hub.")
        return Hub(name, y, x, meta_dict)


class EndHubParser(NodeParser):
    def parse(self) -> End_hub:
        name, y, x, meta_str = self.split_line()
        meta_dict = self.parse_metadata(meta_str) if meta_str else {}
        meta_dict = self.validate_common_meta(meta_dict)
        for k in meta_dict:
            if k not in ["color", "max_drones"]:
                raise ParsingError(f"Invalid key '{k}' for end_hub.")
        return End_hub(name, y, x, meta_dict)


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


class LineValidator:
    def __init__(self, name_file: str) -> None:
        self.fd = open(name_file, "r")
        self.line_number = 0
        self.error_string: str = None

    def next_parser(self, errors: List[str]
                    ) -> Tuple[Optional[BaseParser] | str, Optional[str]]:
        line = self.fd.readline()
        if not line:
            self.fd.close()
            return None, "EOF"
        self.line_number += 1
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
            errors.append(
                f"Line {self.line_number}: "
                f"Unknown configuration token '{key}'")
            return None, "ERROR"


class ConfigParser:
    def __init__(self, name_file: str) -> None:
        self.file_name = name_file
        self.drones: Optional[Drones] = None
        self.start_hub: Optional[Start_hub] = None
        self.hubs: List[Hub] = []
        self.end_hub: Optional[End_hub] = None
        self.connections: List[Connection] = []
        self.errors: List[str] = []

    def print_report(self) -> bool:
        if self.errors:
            string_error = ""
            print(f"\n💥 Found {len(self.errors)} Error(s) in "
                  "configuration file:", file=sys.stderr)
            for error in self.errors:
                string_error += (f" ⚠️  + {error}\n")
            string_error += ("\n❌ Pipeline Status: FAILED\n")
            raise ParsingError(string_error)

    def parse_pipeline(self) -> bool:
        validator = LineValidator(self.file_name)
        while True:
            try:
                parser, status = validator.next_parser(self.errors)
                if status == "EOF":
                    break
                if status == "COMMENT_OR_EMPTY" or not parser:
                    continue
                if status == "ERROR":
                    continue
                result = parser.parse()
                if isinstance(parser, DroneParser):
                    self.drones = result
                elif isinstance(parser, StartHubParser):
                    self.start_hub = result
                elif isinstance(parser, EndHubParser):
                    self.end_hub = result
                elif isinstance(parser, HubParser):
                    self.hubs.append(result)
                elif isinstance(parser, ConnectionParser):
                    self.connections.append(result)
            except (ParsingError, ValueError) as err:
                self.errors.append(f"Line {parser.line_number}: " + str(err))

        self.validate_structural_rules()

        return self.print_report()

    def validate_structural_rules(self) -> None:
        if self.drones is None:
            self.errors.append("Global Error: Missing 'nb_drones' "
                               "definition in the file.")
        if self.start_hub is None:
            self.errors.append("Global Error: Missing 'start_hub' definition. "
                               "The simulation needs a starting point.")
        if self.end_hub is None:
            self.errors.append(
                "Global Error: Missing 'end_hub' definition. "
                "The simulation needs a destination point (goal).")


# parser
# example errors
# -1
# zone not valid
# hub: maze_trap1 1 2 ##[color=
# hub: : 1 2 [color=red]
