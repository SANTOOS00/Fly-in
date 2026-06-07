from typing import List, Dict, Any
from abc import ABC, abstractmethod
# import ParsingError   


class Parsier(ABC):
    @abstractmethod
    def parser_line(slef) -> Dict[str, Any]:
        pass

class ParsingError(Exception):
    def __init__(self, line: int, message: str) -> None:
        super().__init__(f"line {line}: {message}")

class Drones_parsing(Parsier):
    def __init__(self, meta_data) -> None:
        self.meta_data = meta_data

    def parser_line(self) ->Dict:
        pass

class Start_hub_parsing(Parsier):
    def __init__(self, meta_data) -> None:
        self.meta_data = meta_data
    
    def parser_line(self) ->Dict:
        pass

class Hub_parsing(Parsier):
    def __init__(self, meta_data) -> None:
        self.meta_data = meta_data

    def parser_line(self) ->Dict:
        pass

class End_hub_parsing(Parsier):
    def __init__(self, meta_data) -> None:
        self.meta_data = meta_data
    
    def parser_line(self) ->Dict:
        pass        
    
class Connection_parsing(Parsier):
    def __init__(self, meta_data) -> None:
        self.meta_data = meta_data
    
    def parser_line(self) ->Dict:
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
            
            "type_instance": self.type_line(line_str)
        }
        
class Start_hub:
    def __init__(self):
        pass

class Parsing:
    def __init__(self, name_file: str) -> None:
        self.start_hub: Start_hub = None
        self.hub: List[Hub]= []
        self.end_hub: End_hub = None
        self.connection: List[Connection] = []
        self.linevalidator: LineValidator = LineValidator(name_file)

    def parser_args(self) -> None:
        while (True):
            data = self.parser_line()
            if (isinstance(data["type_instance"], Start_hub_parsing)):
                print(data["type_instance"].meta_data)
                break
    # def append_hub(self, hub: Hub) -> None:
    #     pass

    # def append_connection(self, connection: Connection) -> None:
    #     pass