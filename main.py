from parser import Parseline, FlyinError
import sys
from simualtion import Simulation

class Fly_in:
    @staticmethod
    def run() -> None:
        parser = Parseline()
        parser.parse_file()
        # ss = 
        simu = Simulation()
        simu.run()

if __name__ == "__main__":
    try:
        from map import Map
        launcher = Fly_in()
        launcher.run()
        # ss = Map()
        # for hub in ss.hubs.values():
        #     print(hub.name, hub.color, hub.max_drones)
    except FlyinError as error:
        print(error, file=sys.stderr)







