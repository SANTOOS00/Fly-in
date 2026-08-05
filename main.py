from parser import Parseline, FlyinError
import sys
from simualtion import Simulation
from typing import List


class Fly_in:
    def run(self) -> None:
        parser = Parseline()
        parser.parse_file()
        simu = Simulation()
        simu.run()


if __name__ == "__main__":
    try:
        from map import Map
        launcher = Fly_in()
        launcher.run()
        ss = Map()
        for edge in ss.edges:
            print(edge.drones_new)
    except FlyinError as error:
        print(error, file=sys.stderr)
