from custom_error import FlyinError
from modules import Hub, Edge
from map import Map
import re
from parse_meta_data import MetaParser
from base_parse import BaseParser
import sys

try:

    from typing_extensions import override
except ModuleNotFoundError as e:
    print(f"\nMissing module: {e}", file=sys.stderr)
    print("Solution: run the command 'make install'\n", file=sys.stderr)
    exit()


class EdgeParser(BaseParser, MetaParser):
    @override
    def parser(self) -> Edge:
        self._validate_edge_syntax()
        match = re.match(r'^([^\s-]+)-([^\s-]+)(.*)', self.line_str)
        source, destination, *meta = match.groups()
        edge = Edge(
            source=Map().get_hub(source),
            destination=Map().get_hub(destination)
        )
        self.init_meta_data(edge, meta[0])
        return edge

    def _validate_edge_syntax(self) -> None:
        self._validate_source()
        self._validate_destination()

    def _validate_source(self) -> None:
        if not re.match(r'^([^\s-]+)-', self.line_str):
            raise FlyinError('',
                             line_number=str(FlyinError.get_number_line()))

    def _validate_destination(self) -> None:
        if not re.match(r'^([^\s-]+)-([^\s-]+)', self.line_str):
            raise FlyinError('test valid ',
                             line_number=str(FlyinError.get_number_line()))

    def init_meta_data(self, edge: Edge, meta_str: str) -> None:
        if len(meta_str) == 0:
            return None
        meta: dict = self.parse_metadata(meta_str)
        edge.max_link_capacity = int(meta['max_link_capacity'])

    def _valid_max_capacity(self, max_capacity: str) -> int:
        try:
            val_capacity = int(max_capacity)
        except ValueError:
            raise FlyinError('',
                             number_line=str(FlyinError.get_number_line()))
        return val_capacity


class HubParser(BaseParser, MetaParser):
    @override
    def parser(self) -> Hub:
        self._validate_syntax()
        match = re.match(r'^([^\s-]+)\s+(-?\d+)\s+(-?\d+)(.*)',
                         self.line_str)
        name, x, y, *meta = match.groups()
        hub = Hub(
            name=name,
            x=int(x),
            y=int(y),
        )
        self.init_meta_data(hub, meta[0])
        return hub

    def init_meta_data(self, hub: Hub, meta_str: str) -> None:
        if len(meta_str) == 0:
            return None
        meta_dict = self.parse_metadata(meta_str)
        if meta_dict.get('color'):
            hub.color = meta_dict['color']
        if meta_dict.get('zone'):
            hub.zone = hub.Zone.get_type_zone(meta_dict['zone'])
        if meta_dict.get('max_drones'):
            hub.max_drones = int(meta_dict['max_drones'])

    def _validate_syntax(self) -> None:
        self._validate_zone_name()
        self._validate_x_coordinate()
        self._validate_y_coordinate()

    def _validate_zone_name(self):
        if not re.match(r'^([^\s-]+)(\s)', self.line_str):
            raise FlyinError('Zone name is not valid',
                             line_number=str(FlyinError.get_number_line()))

    def _validate_x_coordinate(self):
        if not re.match(r'^([^\s-]+)\s+(-?\d+)', self.line_str):
            raise FlyinError('X coordinate is not valid',
                             line_number=str(FlyinError.get_number_line()))

    def _validate_y_coordinate(self):
        if not re.match(r'^([^\s-]+)\s+(-?\d+)\s+(-?\d+)(.*)', self.line_str):
            raise FlyinError('Y coordinate is not valid',
                             line_number=str(FlyinError.get_number_line()))
