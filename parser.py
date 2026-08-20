from pathlib import Path
from parser_data import HubParser, EdgeParser, FlyinError
from map import Map
from modules import Hub, Edge
import os
import sys


class SafeFileReader:
    def __init__(self, path_file: str):
        self.path_file = Path(path_file)

    def _valid_arg(self) -> None:
        if len(sys.argv) != 2:
            raise FlyinError(
                "Usage: python main.py <file.txt>"
            )

    def valid_path(self):
        self._valid_arg()

        if not self.path_file.exists():
            raise FlyinError(f"File not found: {self.path_file}")

        if not os.access(self.path_file, os.R_OK):
            raise FlyinError(
                f"No read permission: {self.path_file}"
            )


class Parseline:
    def __init__(self) -> None:
        self.raw_line: str
        self.type_line: str
        self.clean_line: str
        self.map = Map()

    def parse_file(self) -> None:
        safe_file = SafeFileReader(sys.argv[1])
        safe_file.valid_path()
        with open(safe_file.path_file, "r") as fb:
            for raw_line in fb:
                self._process_line(raw_line)
            self.map.validate_hub_end_start()
            self.map.valid_number_drones()

    def _process_line(self, raw_line: str):
        FlyinError.add_line_number()
        self.raw_line = raw_line.split("#", maxsplit=1)[0].strip()
        if not self.raw_line:
            return
        self._set_type_line()
        self._dispatch_line()

    def _dispatch_line(self):
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
        hub: Hub = HubParser(self.clean_line.strip()).parser()

        self.map.set_start_hub(hub)

    def _create_hube(self) -> None:
        hub: Hub = HubParser(self.clean_line.strip()).parser()
        self.map.add_hub(hub)

    def _create_end_hube(self) -> None:
        hub: Hub = HubParser(self.clean_line.strip()).parser()
        self.map.set_end_hub(hub)

    def _create_edge(self) -> None:
        edge: Edge = EdgeParser(self.clean_line.strip()).parser()
        self.map.add_egde(edge)

    def _create_number_drones(self) -> None:
        try:
            self.map.set_number_drones(int(self.clean_line))
        except ValueError:
            raise FlyinError("val li  number sahih tabi3i",
                             number_line=str(FlyinError.get_number_line()))

    def _set_type_line(self) -> None:
        if self.raw_line.count(":") < 0:
            raise FlyinError(
                "The line type must match one of the allowed formats "
                "{nb_drones, start_hub, etc.}. Example: [type: ,,, ]",
                number_line=str(FlyinError.get_number_line()))
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
            raise FlyinError('type error',
                             number_line=str(FlyinError.get_number_line()))
