from custom_error import FlyinError
from modules import Hub, Edge
from map import Map
from typing import Dict
import re
from parse_meta_data import MetaParser
from base_parse import BaseParser
import sys

try:
    from typing_extensions import override
except ModuleNotFoundError as e:
    print(f"\nMissing module: {e}", file=sys.stderr)
    print("Solution: run the command 'make install'\n", file=sys.stderr)
    sys.exit(1)


class EdgeParser(BaseParser, MetaParser):
    """Parse a connection line into an Edge object and apply metadata."""

    @override
    def parser(self) -> Edge:
        """Validate syntax and return an Edge instance.

        Returns:
            An Edge connecting two existing hubs from Map.

        Raises:
            FlyinError: When the line syntax is invalid or referenced hubs are
                not defined.
        """
        self._validate_edge_syntax()
        match = re.match(r'^([^\s-]+)-([^\s-]+)(.*)', self.line_str)
        if not match:
            raise FlyinError(f"[ERROR]: Invalid line syntax: {self.line_str}")
        source, destination, *meta = match.groups()
        edge = Edge(
            source=Map().get_hub(source),
            destination=Map().get_hub(destination)
        )
        self.init_meta_data(edge, meta[0])
        return edge

    def _validate_edge_syntax(self) -> None:
        """Ensure both source and destination are present in the line."""
        self._validate_source()
        self._validate_destination()

    def _validate_source(self) -> None:
        """Validate the source portion of the connection syntax."""
        if not re.match(r'^([^\s-]+)-', self.line_str):
            raise FlyinError('[ERROR]: Invalid or missing source format in connection syntax.',
                             line_number=FlyinError.get_number_line())

    def _validate_destination(self) -> None:
        """Validate the destination portion of the connection syntax."""
        if not re.match(r'^([^\s-]+)-([^\s-]+)', self.line_str):
            raise FlyinError("[ERROR]: Invalid destination format! "
                             "Expected format: 'source-destination'",
                             line_number=FlyinError.get_number_line())

    def init_meta_data(self, edge: Edge, meta_str: str) -> None:
        """Apply parsed metadata to the new Edge instance.

        Args:
            edge: Edge object to modify.
            meta_str: Raw metadata substring starting with
            '[' and ending with ']'.
        """
        if len(meta_str) == 0:
            return None
        meta: dict[str, str] | None = self.parse_metadata(meta_str)
        if meta is None:
            return
        edge.max_link_capacity = int(meta['max_link_capacity'])

    def _valid_max_capacity(self, max_capacity: str) -> int:
        """Coerce and validate a max capacity string to integer.

        Raises:
            FlyinError: When the provided value is not a positive integer.
        """
        try:
            val_capacity = int(max_capacity)
        except ValueError:
            raise FlyinError("[ERROR]: Invalid max capacity "
                             f"value '{max_capacity}'! "
                             "Expected a positive integer.",
                             number_line=FlyinError.get_number_line())
        return val_capacity


class HubParser(BaseParser, MetaParser):
    """Parse hub definition lines and apply optional metadata."""

    @override
    def parser(self) -> Hub:
        """Validate syntax and return a Hub instance.

        Returns:
            A Hub object initialized with parsed coordinates and metadata.
        """
        self._validate_syntax()
        match = re.match(r'^([^\s-]+)\s+(-?\d+)\s+(-?\d+)(.*)',
                         self.line_str)
        if not match:
            raise FlyinError(f"Invalid line syntax: {self.line_str}")
        name, x, y, *meta = match.groups()
        hub = Hub(
            name=name,
            x=int(x),
            y=int(y),
        )
        self.init_meta_data(hub, meta[0])
        return hub

    def init_meta_data(self, hub: Hub, meta_str: str) -> None:
        """Apply parsed metadata to the created Hub instance.

        Args:
            hub: Hub object to modify.
            meta_str: Raw metadata substring starting with
            '[' and ending with ']'.
        """
        if len(meta_str) == 0:
            return None
        meta_dict: Dict[str, str] | None = self.parse_metadata(meta_str)
        if meta_dict is None:
            return
        if meta_dict.get('color'):
            hub.color = meta_dict['color']
        if meta_dict.get('zone'):
            hub.zone = hub.Zone.get_type_zone(meta_dict['zone'])
        if "max_drones" in meta_dict.keys():
            hub.max_drones = int(meta_dict['max_drones'])

    def _validate_syntax(self) -> None:
        """Run individual syntax checks for the hub definition."""
        self._validate_zone_name()
        self._validate_x_coordinate()
        self._validate_y_coordinate()

    def _validate_zone_name(self) -> None:
        """Validate the hub's zone/name token is present."""
        if not re.match(r'^([^\s-]+)(\s)', self.line_str):
            raise FlyinError('[ERROR]: Zone name is not valid',
                             line_number=FlyinError.get_number_line())

    def _validate_x_coordinate(self) -> None:
        """Validate the X coordinate token is present and numeric."""
        if not re.match(r'^([^\s-]+)\s+(-?\d+)', self.line_str):
            raise FlyinError('[ERROR]: X coordinate is not valid',
                             line_number=FlyinError.get_number_line())

    def _validate_y_coordinate(self) -> None:
        """Validate the Y coordinate token is present and numeric."""
        if not re.match(r'^([^\s-]+)\s+(-?\d+)\s+(-?\d+)(.*)', self.line_str):
            raise FlyinError('[ERROR]: Y coordinate is not valid',
                             line_number=FlyinError.get_number_line())
