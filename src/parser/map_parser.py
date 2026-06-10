from typing import List, Dict, Any
from abc import ABC, abstractmethod
from simulation import Start_hub, Hub, End_hub, Drones
from parser import ParsingError


class Parsier_meta_data(ABC):
    def __init__(self, meta_data: str, number_line: int) -> None:
        self.meta_data = meta_data
        self.number_line = number_line

    @abstractmethod
    def parser_line(slef) -> Dict[str, Any]:
        pass

    def parser_meta_data(self, meta_string: str) -> Dict[str, str]:
        if not meta_string.startswith("["):
            raise ParsingError(f"Line {self.number_line}: MetaData syntax "
                               f"error. Must start with '[' "
                               f"(found: '{meta_string}')"
                               )
        if not meta_string.endswith("]"):
            raise ParsingError(f"Line {self.number_line}: MetaData syntax "
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
                raise ParsingError(f"Line {self.number_line}: Invalid MetaData" 
                                   f"property '{pair}'. Expected 'key=value'")
            key, value = pair.split("=", 1)
            if not key or not value:
                raise ParsingError(
                    f"Line {self.number_line}: MetaData key "
                    f"or value cannot be empty in '{pair}'"
                    )
            result_dict[key] = value
        return result_dict


class Drones_parsing(Parsier_meta_data):
    def __init__(self, meta_data: str, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> int:
        try:
            number_of_drones: int = 0
            number_of_drones = int(self.meta_data)
            return (Drones(number_of_drones))
        except Exception:
            raise ParsingError(
                f"line: {self.number_line} number in drones is not "
                "in valide this number drones integer")


class Start_hub_parsing(Parsier_meta_data):
    def __init__(self, meta_data: str, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> Start_hub:
        data = self.meta_data.split(" ", 3)
        if len(data) < 4:
            raise ParsingError(
                f"Line {self.number_line}: Missing data. Expected Name, "
                "Y, X, and [MetaData].")
        name = data[0]
        try:
            y = int(data[1])
        except ValueError:
            raise ParsingError(f"Line {self.number_line}: Y coordinate '{data[1]}' must be a valid number.")
        try:
            x = int(data[2])
        except ValueError:
            raise ParsingError(f"Line {self.number_line}: X coordinate '{data[2]}' must be a valid number.")
        meta_data_str = data[3]
        meta_dict = self.parser_meta_data(meta_data_str)
        return Start_hub(name, y, x, meta_dict)

    def parser_meta_data(self, string: str) -> Dict[str, Any]:
        meta_dict: Dict[str, str] = super().parser_meta_data(string)


class Hub_parsing(Parsier_meta_data):
    def __init__(self, meta_data, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> Dict:
        data = self.meta_data.split(" ", 3)
        if len(data) < 4:
            raise ParsingError(f"Line {self.number_line}: Missing data. Expected Name, Y, X, and [MetaData].")
        name = data[0]
        try:
            y = int(data[1])
        except ValueError:
            raise ParsingError(f"Line {self.number_line}: Y coordinate '{data[1]}' must be a valid number.")
        try:
            x = int(data[2])
        except ValueError:
            raise ParsingError(f"Line {self.number_line}: X coordinate '{data[2]}' must be a valid number.")
        meta_data_str = data[3]
        meta_dict = self.parser_meta_data(meta_data_str)
        return Hub(name, y, x, meta_dict)

    def parser_meta_data(self, string: str) -> Dict[str, Any]:
        meta_dict: Dict[str, str] = super().parser_meta_data(string)


class End_hub_parsing(Parsier_meta_data):
    def __init__(self, meta_data, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> Dict:
        data = self.meta_data.split(" ", 3)
        if len(data) < 4:
            raise ParsingError(f"Line {self.number_line}: Missing data. Expected Name, Y, X, and [MetaData].")
        name = data[0]
        try:
            y = int(data[1])
        except ValueError:
            raise ParsingError(f"Line {self.number_line}: Y coordinate '{data[1]}' must be a valid number.")
        try:
            x = int(data[2])
        except ValueError:
            raise ParsingError(f"Line {self.number_line}: X coordinate '{data[2]}' must be a valid number.")
        meta_data_str = data[3]
        meta_dict = self.parser_meta_data(meta_data_str)
        return End_hub(name, y, x, meta_dict)

    def parser_meta_data(self, string: str) -> Dict[str, Any]:
        meta_dict: Dict[str, str] = super().parser_meta_data(string)


class Connection_parsing(Parsier_meta_data):
    def __init__(self, meta_data, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> Dict:
        pass

    def parser_meta_data(self, meta_string):
        meta_dict: Dict[str, str] = super().parser_meta_data(meta_string)


class LineValidator:
    def __init__(self, name_file: str) -> None:
        self.name_file = name_file
        self.number_line = 0
        self.fd = open(name_file, "r")

    def type_line(self, line_str: str) -> ParsingError:
        try:
            if (line_str[0] == "#"):
                return ("#")
            elif (line_str.split(":")[0] == "nb_drones"):
                return (Drones_parsing(line_str.split(":")[1].strip(), self.number_line))
            elif (line_str.split(":")[0] == "start_hub"):
                return (Start_hub_parsing(line_str.split(":")[1].strip(), self.number_line))
            elif (line_str.split(":")[0] == "hub"):
                return (Hub_parsing(line_str.split(":")[1].strip(), self.number_line))
            elif (line_str.split(":")[0] == "end_hub"):
                return (End_hub_parsing(line_str.split(":")[1].strip(), self.number_line))
            elif (line_str.split(":")[0] == "connection"):
                return (Connection_parsing(line_str.split(":")[1].strip(), self.number_line))
            else:
                raise ParsingError(f"line {self.number_line}santax error [nb_drones, .....]")
        except Exception:
            raise ParsingError(f"line {self.number_line} santax error example [nb_drones , ...]:")

    def parser_line(self) -> ParsingError:
        while (True):
            self.number_line += 1
            line_str = self.fd.readline()
            if not line_str:
                self.fd.close()
                return (None)
            if (line_str != '\n'):
                break
        return (self.type_line(line_str))


class Parsing:
    def __init__(self, name_file: str) -> None:
        self.drones: int = 0
        self.start_hub: Start_hub = None
        self.hubs: List = []
        self.end_hub = None
        self.connections: List = []
        self.linevalidator: LineValidator = LineValidator(name_file)

    def parser_args(self) -> None:
        while (True):
            ref_parser = self.linevalidator.parser_line()
            if not ref_parser:
                break
            elif (isinstance(ref_parser, Drones_parsing)):
                self.drones = ref_parser.parser_line()

            elif (isinstance(ref_parser, Start_hub_parsing)):
                self.start_hub = ref_parser.parser_line()

            if (isinstance(ref_parser, Hub_parsing)):
                self.append_hub(ref_parser.parser_line())

            if (isinstance(ref_parser, End_hub_parsing)):
                self.end_hub = ref_parser.parser_line()

    def append_hub(self, hub: Hub) -> None:
        self.hubs.append(hub)
        print(hub.meta)
    # def append_connection(self, connection: Connection) -> None:
    #     self.connections.append(connection)
