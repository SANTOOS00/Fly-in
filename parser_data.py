from typing import Dict, Any, Tuple
# from hube import Hube
from edge import Edge
from abc import ABC

class BaseParser(ABC):
    def __init__(self, line_str: str, line_number: int) -> None:
        self.line_number: int = line_number
        self.line_str: str = line_str

    
    def parser(self) -> None:
        pass


class HubParser(BaseParser):
        patterns = {
            r'^([^\s-]+)(\s)': False,
            r'^([^\s-]+)\s+(-?\d+)': False,
            r'^([^\s-]+)\s+(-?\d+)\s+(-?\d+)(.*)': False,
        }

    # def parser(self) -> None:
    #     pass
    #     # print(self.line_str)
    #     # self._check_syntax(self.line_str.strip())
    #     # match = re.match(r'^(\w+)\s+(-?\d+)\s+(-?\d+)(.*)',
    #     #                  self.line_str.strip())
    #     # name, x, y, *meta = match.groups()
    #     # self.has_invalid_zone_names(name)
    #     # return {
    #     #     "zone_name": name,
    #     #     "x_coordinate": int(x),
    #     #     "y_coordinate": int(y),
    #     #     "metadata": meta[0]
    #     # }

    # def has_invalid_zone_names(self, zone_name) -> None:
    #     pass
    #     # zones: List[str] = ParserConfig.get_all_zone_names()
    #     # if zone_name in zones:
    #     #     raise UtilsError(
    #     #         f"Duplicate zone name '{zone_name}' detected. Each "
    #     #         "zone name must be unique.",
    #     #         self.line_number,
    #     #         ErrorSeverity.Error
    #     #     )

    # def _check_syntax(self, line: str) -> None:
    #     pass
    #     # line = self.line_str.strip()
    #     # for pattern in ZoneWithCoordsParser.patterns.keys():
    #     #     match = re.match(pattern, line)
    #     #     if match is None:
    #     #         ZoneWithCoordsParser.patterns[pattern] = True
    #     #     else:
    #     #         ZoneWithCoordsParser.patterns[pattern] = False
    #     # self._validate_syntax()

    # def _validate_syntax(self) -> None:
    #     pass
    #     # errors = list(ErrorLocation)
    #     # for index, is_not_valid in enumerate(ZoneWithCoordsParser.patterns.
    #     #                                      values()):
    #     #     if is_not_valid:
    #     #         raise ZoneWithCoordsParserError("",
    #     #                                         self.line_number,
    #     #                                         ErrorSeverity.Error,
    #     #                                         errors[index])
        

class EdgeParser(BaseParser):
    def parser(self) -> Edge:
        pass

    def ZoneAdjacencyParser() -> Tuple[str, str]:
        pass