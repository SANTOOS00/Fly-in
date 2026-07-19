from custom_error import FlyinError
from parser import Parseline


class Fly_in:
    @staticmethod
    def run() -> None:
        parser = Parseline()
        parser.parse_line()

if __name__ == "__main__":
    try:
        launcher = Fly_in()
        launcher.run()
    except FlyinError as error:
        error.report()






    # def _get_type_line(self) -> bool:
    #     pass
        # if self.data_str.count(":") != 1:
        #     raise UtilsError(
        #         "The line type must match one of the allowed formats "
        #         "{nb_drones, start_hub, etc.}. Example: [type: ,,, ]",
        #         self.number_line, ErrorSeverity.Error)
        # key_raw, self.clean_line = self.data_str.split(":", 1)
        # self.base_parser = key_raw.lower()
        # parsers = {
        #     "nb_drones": DroneParser,
        #     "start_hub": StartHubParser,
        #     "hub": HubParser,
        #     "end_hub": EndHubParser,
        #     "connection": ConnectionParser
        # }
        # if parsers.get(self.base_parser):
        #     self.base_parser = parsers[self.base_parser]
        #     return True
        # raise Exception()

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

    # @property
    # def get_network(self) -> FlightNetwork:
    #     return self.network

    # @classmethod
    # def append_errors(cls, error) -> None:
    #     cls.instance.errors.append(error)

    # @classmethod
    # def append_warning(cls, error) -> None:
    #     cls.instance.warning.append(error)

    # def print_report(self) -> None:
    #     if self.warning:
    #         string_error = ""
    #         print(f"\n💥 Found {len(self.warning)} Warning(s) in "
    #               "configuration file:", file=sys.stderr)
    #         for error in self.warning:
    #             string_error += (f" ⚠️  + {error}\n")
    #         print(string_error, file=sys.stderr)
    #     if self.errors:
    #         string_error = ""
    #         print(f"\n💥 Found {len(self.errors)} Error(s) in "
    #               "configuration file:", file=sys.stderr)
    #         for error in self.errors:
    #             string_error += (f" ⚠️  + {error}\n")
    #         string_error += ("\n❌ Pipeline Status: FAILED\n")
    #         raise ValueError(string_error)

    # @singledispatchmethod
    # def update_network(self, component):
    #     pass

    # @update_network.register(Drones)
    # def _(self, component: Drones):
    #     self.network.drones = component
    
    # @update_network.register(Start_hub)
    # def _(self, component: Start_hub) -> None:
    #     self.network.start_hube = component
    #     self.network.hubs[component.name] = component

    # @update_network.register(End_hub)
    # def _(self, component: End_hub) -> None:
    #     self.network.end_hube = component
    #     self.network.hubs[component.name] = component

    # @update_network.register(Hub)
    # def _(self, component: Hub | Start_hub | End_hub) -> None:
    #     self.network.hubs[component.name] = component


    # @update_network.register(Connection)
    # def _(self, component: Connection):
    #     self.network.connections.append(component)

    # @classmethod
    # def get_all_zone_names(cls) -> List[str]:
    #     network = cls.instance.network
    #     return list(network.hubs.keys())

    # @classmethod
    # def get_connection(cls) -> List[set[str, str]]:
    #     return [con.connection for con in cls.instance.network.connections]
