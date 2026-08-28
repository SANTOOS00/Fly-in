from pathlib import Path
from parser_data import HubParser, EdgeParser
from custom_error import FlyinError
from map import Map
from modules import Hub, Edge
import os
import sys


class SafeFileReader:
    """Utility to validate the CLI file argument and filesystem access."""

    def __init__(self, path_file: str):
        """Initialize with the provided path string.

        Args:
            path_file: Path to the input file as provided on the CLI.
        """
        self.path_file = Path(path_file)

    def _valid_arg(self) -> None:
        """Ensure exactly one CLI argument (input file) is provided.

        Raises:
            FlyinError: When the number of CLI arguments is incorrect.
        """
        if len(sys.argv) != 2:
            raise FlyinError(
                "[ERROR]: Usage: python main.py <file.txt>"
            )

    def valid_path(self) -> None:
        """Validate that the provided path exists and is readable.

        This calls the internal argument validator and then checks filesystem
        existence and read permission.

        Raises:
            FlyinError: If the file does not exist or is not readable.
        """
        self._valid_arg()

        if not self.path_file.exists():
            raise FlyinError(f"[ERROR]: File not found: {self.path_file}")

        if not os.access(self.path_file, os.R_OK):
            raise FlyinError(
                f"[ERROR]: No read permission: {self.path_file}"
            )


class Parseline:
    """High-level line-oriented parser that dispatches typed lines.

    Parseline reads the input file line-by-line, strips comments, determines
    the line type key, and invokes the correct parser to populate the Map
    singleton with hubs, edges, and drone counts.
    """

    def __init__(self) -> None:
        """Initialize temporary parsing state and reference the global Map."""
        self.raw_line: str
        self.type_line: str
        self.clean_line: str
        self.map = Map()

    def parse_file(self) -> None:
        """Read the CLI-provided file and parse all meaningful lines.

        Raises:
            FlyinError: If file validation fails or parsed content is invalid.
        """
        safe_file = SafeFileReader(sys.argv[1])
        safe_file.valid_path()
        with open(safe_file.path_file, "r") as fb:
            for raw_line in fb:
                self._process_line(raw_line)
            self.map.validate_hub_end_start()

    def _process_line(self, raw_line: str) -> None:
        """Process a single raw input line: strip comments and dispatch.

        Args:
            raw_line: The raw line read from the input file.
        """
        FlyinError.add_line_number()
        self.raw_line = raw_line.split("#", maxsplit=1)[0].strip()
        if not self.raw_line:
            return
        self._set_type_line()
        self._dispatch_line()

    def _dispatch_line(self) -> None:
        """Call the concrete creator based on the parsed type key."""
        match self.type_line.upper():
            case "NB_DRONES":
                self._create_number_drones()
            case "START_HUB":
                self._create_start_hube()
            case "HUB":
                self._create_hube()
            case "END_HUB":
                self._create_end_hube()
            case "CONNECTION":
                self._create_edge()

    def _create_start_hube(self) -> None:
        """Parse and register the start hub from the current clean line."""
        hub: Hub = HubParser(self.clean_line.strip()).parser()

        self.map.set_start_hub(hub)

    def _create_hube(self) -> None:
        """Parse and add a hub to the Map from the current clean line."""
        hub: Hub = HubParser(self.clean_line.strip()).parser()
        self.map.add_hub(hub)

    def _create_end_hube(self) -> None:
        """Parse and register the end hub from the current clean line."""
        hub: Hub = HubParser(self.clean_line.strip()).parser()
        self.map.set_end_hub(hub)

    def _create_edge(self) -> None:
        """Parse and add an edge (connection) to the Map."""
        edge: Edge = EdgeParser(self.clean_line.strip()).parser()
        self.map.add_egde(edge)

    def _create_number_drones(self) -> None:
        """Parse and set the number of drones from the clean line.

        Raises:
            FlyinError: When the number cannot be parsed as an integer.
        """
        try:
            self.map.set_number_drones(int(self.clean_line))
        except ValueError:
            raise FlyinError("[ERROR]: Failed to parse number of drones. The "
                             "value must be a valid integer.",
                             number_line=FlyinError.get_number_line())

    def _set_type_line(self) -> None:
        """Determine the line type key and extract the payload portion.

        The method splits on the first ':' to separate the key from the value
        and maps known keys to the corresponding parser. Unknown keys raise
        FlyinError.
        """
        if self.raw_line.count(":") < 0:
            raise FlyinError(
                "[ERROR]: The line type must match one of the allowed formats "
                "{nb_drones, start_hub, etc.}. Example: [type: ,,, ]",
                number_line=FlyinError.get_number_line())
        key_raw, self.clean_line = self.raw_line.split(":", 1)
        parsers = {
            "nb_drones": 'DroneParser',
            "start_hub": HubParser,
            "hub": HubParser,
            "end_hub": HubParser,
            "connection": EdgeParser
        }
        if parsers.get(key_raw.lower()):
            self.type_line = key_raw.lower()
        else:
            raise FlyinError(f"[ERROR]: Unknown line type '{key_raw.strip()}'. "
                             f"Must be one of {set(parsers.keys())}.",
                             number_line=FlyinError.get_number_line())
