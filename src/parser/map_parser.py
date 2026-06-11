from typing import List, Dict, Any
from abc import ABC, abstractmethod
from simulation import Start_hub, Hub, End_hub, Drones, Connection
from .custom_error import ParsingError
from utils import get_hex, allowed_status


class BaseParser(ABC):
    def __init__(self, raw_line: str, line_number: int) -> None:
        self.raw_line = raw_line
        self.line_number = line_number

    @abstractmethod
    def parse(self) -> Any:
        pass

    def parse_metadata(self, meta_string: str) -> Dict[str, str]:
        if not meta_string.startswith("["):
            raise ParsingError(f"Line {self.line_number}: MetaData syntax "
                               f"error. Must start with '[' "
                               f"(found: '{meta_string}')"
                               )
        if not meta_string.endswith("]"):
            raise ParsingError(f"Line {self.line_number}: MetaData syntax "
                               f"error. Missing closing bracket ']' at the "
                               f"end of '{meta_string}'"
                               )
        content = meta_string[1:-1]
        result_dict = {}
        if not content:
            return result_dict
        pairs = content.split()
        for pair in pairs:
            if "=" not in pair:
                raise ParsingError(f"Line {self.line_number}: Invalid MetaData" 
                                   f"property '{pair}'. Expected 'key=value'")
            key, value = pair.split("=", 1)
            if not key or not value:
                raise ParsingError(
                    f"Line {self.line_number}: MetaData key "
                    f"or value cannot be empty in '{pair}'"
                    )
            result_dict[key] = value
        return result_dict


class DroneParser(BaseParser):
    def __init__(self, raw_line: str, line_number: int) -> None:
        super().__init__(raw_line, line_number)

    def parse(self) -> int:
        try:
            number_of_drones = int(self.raw_line)
            return (Drones(number_of_drones))
        except Exception:
            raise ParsingError(
                f"line: {self.line_number} number in drones is not "
                "in valide this number drones integer")


class StartHubParser(BaseParser):
    def __init__(self, raw_line: str, line_number: int) -> None:
        super().__init__(raw_line, line_number)

    def parse(self) -> Start_hub:
        data = self.raw_line.split(" ", 3)
        name = data[0]
        try:
            y = int(data[1])
        except ValueError:
            raise ParsingError(f"Line {self.line_number}: Y coordinate "
                               f"'{data[1]}' must be a valid number.")
        try:
            x = int(data[2])
        except ValueError:
            raise ParsingError(f"Line {self.line_number}: X coordinate "
                               f"'{data[2]}' must be a valid number.")
        meta_data_str = data[3]
        meta_dict = self.parse_metadata(meta_data_str)
        return Start_hub(name, y, x, meta_dict)

    def parse_metadata(self, string: str) -> Dict[str, Any]:
        meta_dict: Dict[str, str] = super().parse_metadata(string)
        if meta_dict.get("max_drones"):
            try:
                meta_dict["max_drones"] = int(meta_dict["max_drones"])
            except ValueError:
                raise ValueError(
                    f"Line {self.line_number}: Invalid value for "
                    f"'max_drones' -> '{meta_dict['max_drones']}'. "
                    "Expected an integer.")
        for k, v in meta_dict.items():
            if k == "color":
                meta_dict["color"] = get_hex(v, self.line_number)
            elif k == "max_drones":
                continue
            else:
                raise ParsingError(
                    f"Line {self.line_number}: Invalid meta key '{k}'. "
                    "Allowed keys: color, max_drones")
        return meta_dict


class HubParser(BaseParser):
    def __init__(self, raw_line, line_number: int) -> None:
        super().__init__(raw_line, line_number)

    def parse(self) -> Dict:
        data = self.raw_line.split(" ", 3)
        name = data[0]
        try:
            y = int(data[1])
        except ValueError:
            raise ParsingError(f"Line {self.line_number}: Y coordinate "
                               "'{data[1]}' must be a valid number.")
        try:
            x = int(data[2])
        except ValueError:
            raise ParsingError(f"Line {self.line_number}: X coordinate "
                               "'{data[2]}' must be a valid number.")
        meta_data_str = data[3]
        meta_dict = self.parse_metadata(meta_data_str)
        return Hub(name, y, x, meta_dict)

    def parse_metadata(self, string: str) -> Dict[str, Any]:
        meta_dict: Dict[str, str] = super().parse_metadata(string)
        if meta_dict.get("max_drones"):
            try:
                meta_dict["max_drones"] = int(meta_dict["max_drones"])
            except ValueError:
                raise ValueError(
                    f"Line {self.line_number}: Invalid value for "
                    f"'max_drones' -> '{meta_dict['max_drones']}'. "
                    "Expected an integer.")
        for k, v in meta_dict.items():
            if k == "color":
                meta_dict["color"] = get_hex(v, self.line_number)
            elif k == "zone":
                meta_dict["zone"] = allowed_status(v, self.line_number)
            elif k == "max_drones":
                continue
            else:
                raise ParsingError(
                    f"Line {self.line_number}: Invalid meta key '{k}'. "
                    "Allowed keys: color, max_drones")
        return meta_dict


class EndHubParser(BaseParser):
    def __init__(self, raw_line, line_number: int) -> None:
        super().__init__(raw_line, line_number)

    def parse(self) -> Dict:
        data = self.raw_line.split(" ", 3)
        name = data[0]
        try:
            y = int(data[1])
        except ValueError:
            raise ParsingError(f"Line {self.line_number}: Y coordinate "
                               f"'{data[1]}' must be a valid number.")
        try:
            x = int(data[2])
        except ValueError:
            raise ParsingError(f"Line {self.line_number}: X coordinate "
                               f"'{data[2]}' must be a valid number.")
        meta_data_str = data[3]
        meta_dict = self.parse_metadata(meta_data_str)
        return End_hub(name, y, x, meta_dict)

    def parse_metadata(self, string: str) -> Dict[str, Any]:
        meta_dict: Dict[str, str] = super().parse_metadata(string)
        if meta_dict.get("max_drones"):
            try:
                meta_dict["max_drones"] = int(meta_dict["max_drones"])
            except ValueError:
                raise ValueError(
                    f"Line {self.line_number}: Invalid value for "
                    f"'max_drones' -> '{meta_dict['max_drones']}'. "
                    "Expected an integer.")
        for k, v in meta_dict.items():
            if k == "color":
                meta_dict["color"] = get_hex(v, self.line_number)
            elif k == "max_drones":
                continue
            else:
                raise ParsingError(
                    f"Line {self.line_number}: Invalid meta key '{k}'. "
                    "Allowed keys: color, max_drones")
        return meta_dict


class ConnectionParser(BaseParser):
    def __init__(self, raw_line, line_number: int) -> None:
        super().__init__(raw_line, line_number)

    def parse(self) -> Dict:
        if self.raw_line is None:
            raise ParsingError(
                f"Line {self.line_number}:"
                "invalid connection "
                f"{self.raw_line}. Expected format 'node1-node2 [key=value]'"
            )
        if "-" not in self.raw_line:
            raise ParsingError(
                f"Line {self.line_number}:"
                "invalid connection "
                f"{self.raw_line}. Expected format 'node1-node2 [key=value]'"
            )
        # meta = self.raw_line.split()
        # print(meta)
        return (Connection())

    def parser_meta_data(self, meta_string):
        meta_dict: Dict[str, str] = super().parse_metadata(meta_string)
        return meta_dict


class LineValidator:
    def __init__(self, name_file: str) -> None:
        self.name_file = name_file
        self.line_number = 0
        self.fd = open(name_file, "r")

    def detect_line_type(self, line_str: str) -> ParsingError | None:
        try:
            key = line_str.split(":")[0].strip()
            print(line_str.split(":")[1])
            if line_str.startswith("#"):
                return None
            elif key == "nb_drones":
                return DroneParser(
                    line_str.split(":")[1].strip(), self.line_number)
            elif key == "start_hub":
                return StartHubParser(
                    line_str.split(":")[1].strip(), self.line_number)
            elif key == "hub":
                return HubParser(
                    line_str.split(":")[1].strip(), self.line_number)
            elif key == "end_hub":
                return EndHubParser(
                    line_str.split(":")[1].strip(), self.line_number)
            elif key == "connection":
                return ConnectionParser(
                    line_str.split(":")[1].strip(), self.line_number)
            else:
                raise ParsingError(
                    f"Line {self.line_number}: Invalid keyword '{key}'. "
                    "Expected one of [nb_drones, start_hub, "
                    "hub, end_hub, connection]"
                )
        except Exception:
            raise ParsingError(
                        f"Line {self.line_number}: Syntax error. "
                        "Expected format 'key: value'.")

    def validate(self) -> ParsingError:
        while (True):
            self.line_number += 1
            line_str = self.fd.readline()
            if not line_str:
                self.fd.close()
                return (None)
            if (line_str != '\n'):
                break
            self.detect_line_type(line_str)
        return (self.detect_line_type(line_str))


class ConfigParser:
    def __init__(self, name_file: str) -> None:
        self.drones: int = 0
        self.start_hub: Start_hub = None
        self.hubs: List = []
        self.end_hub = None
        self.connections: List = []
        self.linevalidator: LineValidator = LineValidator(name_file)

    def parse(self) -> None:
        while (True):
            ref_parser = self.linevalidator.validate()
            if not ref_parser:
                break
            elif (isinstance(ref_parser, DroneParser)):
                self.drones = ref_parser.parse()

            elif (isinstance(ref_parser, StartHubParser)):
                self.start_hub = ref_parser.parse()

            elif (isinstance(ref_parser, HubParser)):
                self.append_hub(ref_parser.parse())

            elif (isinstance(ref_parser, EndHubParser)):
                self.end_hub = ref_parser.parse()

            elif (isinstance(ref_parser, ConnectionParser)):
                self.append_connection(ref_parser.parse())

    def append_hub(self, hub: Hub) -> None:
        self.hubs.append(hub)

    def append_connection(self, connection: Connection) -> None:
        self.connections.append(connection)
        
