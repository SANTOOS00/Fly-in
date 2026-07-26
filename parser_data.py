from custom_error import FlyinError
from typing import Tuple, List
from typing_extensions import override
from modules import Hub, Edge
from map import Map
import re


class BaseParser:
    def __init__(self, line_str: str) -> None:
        self.line_str: str = line_str

    @override
    def parser(self) -> None:
        pass

class EdgeParser(BaseParser):
    @override
    def parser(self) -> Edge:
        self._validate_edge_syntax()
        match = re.match(r'^([^\s-]+)-([^\s-]+)(.*)', self.line_str)
        source, destination, *meta = match.groups()
        edge = Edge(
            source=Map().get_hub(source),
            destintion=Map().get_hub(destination)
        )
        return edge


    def _validate_edge_syntax(self) -> None:
        self._validate_source()
        self._validate_destination()    

    def _validate_source(self) -> None:
        if not re.match(r'^([^\s-]+)-', self.line_str):
            raise FlyinError('',
                             line_number=FlyinError.get_number_line)

    def _validate_destination(self) -> None:
        if not re.match(r'^([^\s-]+)-([^\s-]+)', self.line_str):
            raise FlyinError('test valid ',
                             line_number=FlyinError.get_number_line)


    def ZoneAdjacencyParser() -> Tuple[str, str]:
        pass



class HubParser(BaseParser):
    @override
    def parser(self) -> Hub:
        self._validate_syntax()
        match = re.match(r'^(\w+)\s+(-?\d+)\s+(-?\d+)(.*)',
                        self.line_str)
        name, x, y, *meta = match.groups()
        hub = Hub(
            name=name,
            x=int(x),
            y=int(y),
        )
        self.init_meta_data(hub, meta)
        return hub

    
    def init_meta_data(self, hub: Hub, meta: List[str]) -> None:
        pass

    def _validate_syntax(self) -> None:
        self._validate_zone_name()
        self._validate_x_coordinate()
        self._validate_y_coordinate()

    def _validate_zone_name(self):
        if not re.match(r'^([^\s-]+)(\s)', self.line_str):
            raise FlyinError('Zone name is not valid',
                             number_line=FlyinError.get_number_line())

    def _validate_x_coordinate(self):
        if not re.match(r'^([^\s-]+)\s+(-?\d+)', self.line_str):
            raise FlyinError('X coordinate is not valid',
                             number_line=FlyinError.get_number_line())


    def _validate_y_coordinate(self):
        if not re.match(r'^([^\s-]+)\s+(-?\d+)\s+(-?\d+)(.*)', self.line_str):
            raise FlyinError('Y coordinate is not valid',
                             number_line=FlyinError.get_number_line())



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




#################################################
################################################
# class MetaParser:
#     patternsmetadata = {
#         r'^\s*\w+=[a-zA-Z0-9]+': False,
#         r'^\s*\w+=[a-zA-Z0-9]+(\s+\w+=[a-zA-Z0-9]+)?': False,
#         r'^\s*\w+=[a-zA-Z0-9]+(\s+\w+=[a-zA-Z0-9]+)?(\s+\w+=[a-zA-Z0-9]+)?$': False,
#         r'^\s*\w+=[a-zA-Z0-9]+(\s+\w+=[a-zA-Z0-9]+)*\s*$': False,
#     }
#     def __init__(self) -> None:
#         self.match: re.Match
#         self.typ_obj: BaseError

#     def parse_metadata(self, meta_data: str) -> Dict[str, str]:
#         if len(meta_data) == 0:
#             return (self._default_val())
#         meta_data = self._validate_metadata_format(meta_data)
#         if len(meta_data) == 0:
#             return (self._default_val())
#         self._check_syntax_meta(meta_data)

#         valid_meta = MetadataValidator(self.line_number,
#                                        self,
#                                        self._split_key_values())
#         return (valid_meta.validate_metadata())

#     @staticmethod
#     def check_duplicates(data: tuple[str], line_nu: int) -> None:
#         seen = set()
#         for itm in [k.split("=")[0].strip() for k in data]:
#             if itm in seen:
#                 raise MetaDataParserError(f"Duplicate metadata item '{itm}',"
#                                           " The first occurrence will "
#                                           "be used.",
#                                           line_nu,
#                                           ErrorSeverity.Warning
#                                           )
#             else:
#                 seen.add(itm)

#     def _split_key_values(self) -> Dict[str, str]:
#         data: str = self.match.group().split()
#         try:
#             MetaParser.check_duplicates(data, self.line_number)
#         except Exception as error:
#             ParserConfig.append_warning(error)

#         return (
#             {key.lower().strip(): val
#                 for keyval in data
#                 for key, val in [keyval.split("=")]}
#         )

#     def _validate_metadata_format(self, meta_data: str) -> str:
#         meta_string = meta_data.strip()
#         if not meta_string.startswith("["):
#             raise MetaDataParserError("MetaData must start with '['",
#                                       self.line_number,
#                                       ErrorSeverity.Error)
#         if not meta_string.endswith("]"):
#             raise MetaDataParserError("MetaData missing closing bracket ']'",
#                                       self.line_number,
#                                       ErrorSeverity.Error)
#         return (meta_string[1:-1].strip())

#     def _check_syntax_meta(self, meta_data) -> None:
#         for pattern in MetaParser.patternsmetadata:
#             match = re.match(pattern, meta_data)
#             if match is None:
#                 MetaParser.patternsmetadata[pattern] = True
#             else:
#                 MetaParser.patternsmetadata[pattern] = False
#         self._validate_syntax_meta(meta_data.split())
#         self.match = match

#     def _default_val(self) -> dict[str, int]:
#         if isinstance(self, ConnectionParser):
#             return {
#                 "max_link_capacity": 1
#             }
#         else:
#             return {
#                 "max_drones": 1
#             }

#     def _validate_syntax_meta(self, data: List[str]) -> None:
#         for index, is_not_valid in enumerate(MetaParser.patternsmetadata.
#                                              values()):
#             if is_not_valid:
#                 raise MetaDataParserError("Invalid MetaData property syntax at"
#                                           f" position {data[index]}. Expected "
#                                           "format: ''.",
#                                           self.line_number,
#                                           ErrorSeverity.Error,
#                                           )


###################################################333
##################################################33333
# class MetadataValidator:
#     def __init__(self,
#                  line_number: int,
#                  in_type: BaseParser,
#                  data: Dict[str, Any]) -> None:
#         self.line_number = line_number
#         self.in_type = in_type
#         self.data = data

#     @property
#     def get_color(self) -> str:
#         return self.data['color']

#     @property
#     def get_name_zone(self) -> str:
#         return self.data['zone']

#     @property
#     def get_max_drones(self) -> int:
#         try:
#             val = int(self.data['max_drones'])
#             if val < 0:
#                 raise MetaDataParserError(
#                     "Invalid value for 'max_drones' in metadata: "
#                     f"{self.data['max_drones']}",
#                     self.line_number,
#                     ErrorSeverity.Error
#                     )
#             return val
#         except Exception:
#             raise MetaDataParserError(
#                 "Invalid value for 'max_drones' in metadata: "
#                 f"{self.data['max_drones']}",
#                 self.line_number,
#                 ErrorSeverity.Error
#             )

#     @property
#     def get_link_capacity(self) -> int:
#         try:
#             val = int(self.data['max_link_capacity'])
#             if val < 0:
#                 raise MetaDataParserError(
#                     "Invalid value for 'max_link_capacity' in metadata: "
#                     f"{self.data['max_link_capacity']}. "
#                     "It must be an integer greater than or equal to 1.",
#                     self.line_number,
#                     ErrorSeverity.Error
#                     )
#             return val
#         except Exception:
#             raise MetaDataParserError(
#                 "Invalid value for 'max_link_capacity' in metadata: "
#                 f"{self.data['max_link_capacity']}. "
#                 "It must be an integer greater than or equal to 1.",
#                 self.line_number,
#                 ErrorSeverity.Error
#             )

#     @property
#     def _set_color(self) -> None:
#         if self.data.get('color'):
#             self.data["color"] = self.get_hex(self.get_color)
#         else:
#             self.data["color"] = self.get_hex('white')

#     @property
#     def _set_type_zone(self) -> None:
#         if self.data.get('zone'):
#             self.data['zone'] = self.allowed_status_zone(self.get_name_zone)
#         else:
#             self.data['zone'] = self.allowed_status_zone('normal')

#     @property
#     def _set_max_drones(self) -> None:
#         if self.data.get('max_drones'):
#             self.data['max_drones'] = self.get_max_drones
#         else:
#             self.data['max_drones'] = 1
    
#     @property
#     def _set_max_capacity(self) -> None:
#         if self.data.get('max_link_capacity'):
#             self.data['max_link_capacity'] = self.get_link_capacity

#     def validate_metadata(self) -> Dict[str, Any]:
#         self.allowed_status_meta()
#         if isinstance(self.in_type, ConnectionParser):
#             self._set_max_capacity
#         else:
#             self._set_color
#             self._set_type_zone
#             self._set_max_drones
#         return (self.data)

#     def get_hex(self, color: str) -> str:
#         try:
#             c = Color(color.lower())
#             return COLOR_HEX[c]
#         except ValueError:
#             return "#FFFFFF"

#     def allowed_status_zone(self, status_zone: str) -> str:
#         status = status_zone.lower()
#         for allowed in Type_zone:
#             if status == allowed.value[0][1]:
#                 return allowed.value[0][0]
#         raise UtilsError(
#             f"Invalid status_zone '{status}'. Allowed values: "
#             f"{', '.join(allowed)}",
#             self.line_number,
#             ErrorSeverity.Error,
#         )

#     def allowed_status_meta(self) -> None:
#         allowed = ["zone", "color", "max_drones"]
#         if isinstance(self.in_type, ConnectionParser):
#             for key in self.data.keys():
#                 if key not in "max_link_capacity":
#                     raise MetaDataParserError(
#                         "Invalid connection metadata\n \n ⚠ Fix: "
#                         f"key '{self.data}'"
#                         f"allowed \n 'max_link_capacity' just",
#                         self.line_number,
#                         ErrorSeverity.Error)
#         else:
#             for key in self.data.keys():
#                 if key not in allowed:
#                     raise MetaDataParserError(
#                         "Invalid connection metadata\n \n ⚠ "
#                         f"Fix: key '{self.data}'"
#                         f"\n           allowed       \n'{allowed}'\n "
#                         "           just",
#                         self.line_number,
#                         ErrorSeverity.Error)

