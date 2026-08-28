from typing import List, Dict, Optional
from modules import Hub, Edge
from custom_error import FlyinError


class Map:
    """Singleton container for the parsed map data (hubs, edges, drone count).

    Map stores the network definition and provides helpers to access and
    validate the configuration required by the simulation.
    """

    _instance: Optional['Map'] = None
    _initialized: bool = False

    def __new__(cls) -> 'Map':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the singleton storage on first construction."""
        if Map._initialized is True:
            return
        Map._initialized = True
        self.number_drones: int = -1
        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None
        self.hubs: Dict[str, Hub] = {}
        self.edges: List[Edge] = []

    def get_start(self) -> Hub | None:
        """Return the configured start hub or None if not set."""
        return self.start_hub

    def get_end(self) -> Hub | None:
        """Return the configured end hub or None if not set."""
        return self.end_hub

    def add_hub(self, hub: Hub) -> None:
        """Add a hub to the map, erroring on duplicates.

        Args:
            hub: Hub to register.

        Raises:
            FlyinError: When a hub with the same name already exists.
        """
        if self.hubs.get(hub.name):
            raise FlyinError(f'[ERROR]: Duplicate hub => {hub.name}',
                             line_number=FlyinError.get_number_line())
        self.hubs[hub.name] = hub

    def set_start_hub(self, start_hub: Hub) -> None:
        """Set and register the start hub (only allowed once)."""
        if self.start_hub is not None:
            raise FlyinError('[ERROR]: Duplicate start hub',
                             line_number=FlyinError.get_number_line())
        self.start_hub = start_hub
        self.add_hub(start_hub)

    def set_end_hub(self, end_hub: Hub) -> None:
        """Set and register the end hub, updating its capacity
        to total drones."""
        if self.end_hub is not None:
            raise FlyinError('[ERROR]: Duplicate end hub',
                             line_number=FlyinError.get_number_line())
        self.end_hub = end_hub
        self.end_hub.max_drones = Map().number_drones
        self.add_hub(end_hub)

    def add_egde(self, edge: Edge) -> None:
        """Append an Edge to the map ensuring no duplicate undirected links.

        Args:
            edge: Edge instance to add.

        Raises:
            FlyinError: When an equivalent undirected edge already exists.
        """
        if {edge.source, edge.destination} in [{edg.source, edg.destination}
                                               for edg in self.edges]:
            raise FlyinError("[ERROR]: Duplicate edge detected between "
                             f"'{edge.source}' and '{edge.destination}'!",
                             line_number=FlyinError.get_number_line())
        self.edges.append(edge)

    def validate_hub_end_start(self) -> None:
        """Ensure both start and end hubs are configured.

        Raises:
            FlyinError: When either start or end hub is missing.
        """
        if self.number_drones == -1:
            raise FlyinError("[ERROR]: Number of drones has not been set. "
                             "Please define 'nb_drones: <integer>' in your configuration.")
        if self.start_hub is None:
            raise FlyinError(
                "[Error]: Missing Start Hub! You must define at least "
                "one start hub using this format:"
                "start_hub: name_zone x y [key=val]",
                number_line=FlyinError.get_number_line()
            )
        if self.end_hub is None:
            raise FlyinError(
                "[Error]: Missing End Hub! You must define at least "
                "one end hub using this format:"
                "end_hub: name_zone x y [key=val]",
                number_line=FlyinError.get_number_line()
            )

    def get_hub(self, name_zone: str) -> Hub:
        """Return the Hub instance by name, raising when missing.

        Args:
            name_zone: Hub name/key to lookup.

        Returns:
            The Hub instance from the map.

        Raises:
            FlyinError: When the named hub is not defined.
        """
        if not self.hubs.get(name_zone):
            raise FlyinError(f"[ERROR]: Zone name '{name_zone}' is not defined "
                             "in the configuration file.",
                             line_number=FlyinError.get_number_line())
        return self.hubs[name_zone]

    def set_number_drones(self, number_drones: int) -> None:
        """Set the global number of drones for the simulation.

        Args:
            number_drones: Integer number of drones to set.

        Raises:
            FlyinError: When the number has already been set or is invalid.
        """
        print(number_drones)
        if number_drones < 1:
            raise FlyinError('[ERROR]: number of drones is not valid. Minimum required value is 1.',
                             line_number=FlyinError.get_number_line())
        self.number_drones = number_drones
