from typing import List, Dict, Any
from abc import ABC, abstractmethod


class Parsier_meta_data(ABC):
    def __init__(self, meta_data: str, number_line: int) -> None:
        self.meta_data = meta_data
        self.number_line = number_line

    @abstractmethod
    def parser_line(slef) -> Dict[str, Any]:
        pass


class Start_hub:
    def __init__(self, name: str, y: int, x: int, meta: str | None = None
                 ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.meta: Dict[str: Any] | None = meta


class Drones:
    def __init__(self, number_drones: int) -> None:
        self.number_drones = number_drones


class ParsingError(Exception):
    def __init__(self, massege: str) -> None:
        super().__init__(massege)


class Drones_parsing(Parsier_meta_data):
    def __init__(self, meta_data: str, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> int:
        try:
            number_of_drones: int = 0
            number_of_drones = int(self.meta_data)
            return (Drones(number_of_drones))
        except Exception:
            raise ParsingError(f"line: {self.number_line} number in drones is not in valide this number drones integer")


class Start_hub_parsing(Parsier_meta_data):
    def __init__(self, meta_data: str, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> Start_hub:
        if not self.meta_data:
            raise ParsingError(f"len {self.number_line} line is not invalide")
        # pattern = r"(\w+)\s+(\d+)\s+(\d+)\s+(.+)?"
        # name = match.group(1)
        # try:
        #     y = int(match.group(2))
        # except ValueError:
        #     raise ParsingError(f"{self.number_line} number in y not in valide")
        # try:
        #     x = int(match.group(3))
        # except ValueError:
        #     raise ParsingError(f"{self.number_line} number in x not in valide")

        # meta = match.group(4)
        # print(match)
        return (Start_hub(name, y, x, meta))


class Hub_parsing(Parsier_meta_data):
    def __init__(self, meta_data, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> Dict:
        pass


class End_hub_parsing(Parsier_meta_data):
    def __init__(self, meta_data, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> Dict:
        pass


class Connection_parsing(Parsier_meta_data):
    def __init__(self, meta_data, number_line: int) -> None:
        super().__init__(meta_data, number_line)

    def parser_line(self) -> Dict:
        pass


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

            # if (isinstance(data["type_instance"], End_hub_parsing)):
            #     self.start_hub = data["type_instance"].parser_line()

            # if (isinstance(data["type_instance"], Connection_parsing)):
            #     self.start_hub = data["type_instance"].parser_line()
        print(self.start_hub.meta)
    # def append_hub(self, hub: Hub) -> None:
    #     pass

    # def append_connection(self, connection: Connection) -> None:
    #     pass