from parser import Parseline
from custom_error import FlyinError
import sys
from simualtion import Simulation


class Fly_in:
    def run(self) -> None:
        parser = Parseline()
        parser.parse_file()
        simu = Simulation()
        simu.run()


if __name__ == "__main__":
    try:
        launcher = Fly_in()
        launcher.run()
    except FlyinError as error:
        print(error, file=sys.stderr)
