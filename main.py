from parser import Parseline, FlyinError
import sys
from simualtion import Simulation

class Fly_in:
    @staticmethod
    def run() -> None:
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







