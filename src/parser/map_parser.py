from typing import List, Dict, Any
from abs import ABS, abstractmethod
# import ParsingError   


class Parsing(ABC)
    @abstractmethod
    def parser_line(slef) -> Dict[str, Any]:
        pass

class ParsingError(Exception):
    def __init__(self, line: int, message: str) -> None:
        super().__init__(f"line {line}: {message}")

class Drones_parsing(Parsing):
    def __init__(self, meta_data) -> None:
        pass

class Start_hub_parsing(Parsing):
    def __init__(self, meta_data) -> None:
        pass

class Hub_parsing(Parsing):
    def __init__(self, meta_data) -> None:
        pass

class End_hub_parsing(Parsing):
    def __init__(self, meta_data) -> None:
        pass
    
class Connection_parsing(Parsing):
    def __init__(self, meta_data) -> None:
        pass
  
class LineValidator:
    def __init__(self, name_file: str) -> None:
        self.name_file = name_file
        self.number_line = 0
        self.fd = open(name_file, "r")

    def type_line(self , line_str: str) -> None:
        try:
            if (line_str[0] == "#"):
                return ("#")
            elif (line_str.split(":")[0] == "nb_drones"):
                return (Drones_parsing(line_str.split(":")[1]))
            elif (line_str.split(":")[0] == "start_hub"):
                return (Start_hub_parsing(line_str.split(":")[1]))
            elif (line_str.split(":")[0] == "hub"):
                return (Hub_parsing(line_str.split(":")[1]))
            elif (line_str.split(":")[0] == "end_hub"):
                return (End_hub_parsing(line_str.split(":")[1]))
            elif (line_str.split(":")[0] == "connection"):
                return (Connection_parsing(line_str.split(":")[1]))
            else:
                raise ParsingError(self.number_line, "test string")
        except Exception as error:
            raise ParsingError(self.number_line, "test error")

    def parser_line(self) -> Dict[str, Any]:
        while(True):
            self.number_line += 1
            line_str = self.fd.readline()
            if not line_str:
                return (None)
            if (line_str != '\n'):
                break
        return {
            "line": self.number_line,
            "type_insetince": self.type_line(line_str)
        }
class Parsing:
    def __init__(self, name_file: str) -> None:
        self.start_hub: Start_hub = None
        self.hub: List[Hub]= []
        self.end_hub: End_hub = None
        self.connection: List[connection] = []
        self.linevalidator: LineValidator = LineValidator(name_file)

    def parser_args(self) -> None:
        print(self.linevalidator.parser_line())
        print(self.linevalidator.parser_line())
        print(self.linevalidator.parser_line())
        print(self.linevalidator.parser_line())
        print(self.linevalidator.parser_line())
        print(self.linevalidator.parser_line())
        print(self.linevalidator.parser_line())
        print(self.linevalidator.parser_line())
        print(self.linevalidator.parser_line())
        print(self.linevalidator.parser_line())

