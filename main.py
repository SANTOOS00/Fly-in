from parser import Parseline, FlyinError
import sys
from simualtion import Simulation
from map import Map
class Fly_in:
    @staticmethod
    def run() -> None:
        parser = Parseline()
        parser.parse_file()
        simu = Simulation(
            Map().number_drones,
            Map().get_start())
        simu.run()
if __name__ == "__main__":
    try:
        launcher = Fly_in()
        launcher.run()
    except FlyinError as error:
        print(error, file=sys.stderr)







