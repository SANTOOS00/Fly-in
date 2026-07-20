from custom_error import FlyinError
from typing import Tuple
from edge import Edge
from hube import Hub
import re


class BaseParser:
    def __init__(self, line_str: str) -> None:
        self.line_str: str = line_str.strip()

    def parser(self) -> None:
        pass

class EdgeParser(BaseParser):
    def parser(self) -> Edge:
        print(self.line_str)

    def ZoneAdjacencyParser() -> Tuple[str, str]:
        pass


class HubParser(BaseParser):
    def parser(self) -> None:
        self._validate_syntax()
        match = re.match(r'^(\w+)\s+(-?\d+)\s+(-?\d+)(.*)',
                        self.line_str)
        name, x, y, *meta = match.groups()
        return Hub(
            name=name,
            x=int(x),
            y=int(y),
        )

    def _validate_syntax(self) -> None:
        self._validate_zone_name()
        self._validate_x_coordinate()
        self._validate_y_coordinate()


    FlyinError.check_error(type_error='Zone name')
    def _validate_zone_name(self):
        if not re.match(r'^([^\s-]+)(\s)', self.line_str):
            raise FlyinError('Zone name is not valid',
                             number_line=FlyinError.get_number_line())



    FlyinError.check_error(type_error='X')
    def _validate_x_coordinate(self):
        if not re.match(r'^([^\s-]+)\s+(-?\d+)', self.line_str):
            raise FlyinError('X coordinate is not valid',
                             number_line=FlyinError.get_number_line())


    FlyinError.check_error(type_error='Y')
    def _validate_y_coordinate(self):
        if not re.match(r'^([^\s-]+)\s+(-?\d+)\s+(-?\d+)(.*)', self.line_str):
            raise FlyinError('Y coordinate is not valid',
                             number_line=FlyinError.get_number_line())



# class ErrorLocation(Enum):
#     ZONE = "Zone name is not valid"
#     X_AXIS = "X coordinate is not valid"
#     Y_AXIS = "Y coordinate is not valid"
    # @property
    # def validate_hub_end_start(self) -> None:
    #     if self.network.start_hube is None:
    #         raise ValueError(
    #             "[Error]: Missing Start Hub! \n  You must define at least "
    #             "one start hub using this format:\n"
    #             "    >> start_hub: name_zone x y [key=val] <<"
    #         )
    #     if self.network.end_hube is None:
    #         raise ValueError(
    #             "[Error]: Missing End Hub! \n  You must define at least "
    #             "one end hub using this format:\n"
    #             "     >> start_end: name_zone x y [key=val] <<"
    #         )
