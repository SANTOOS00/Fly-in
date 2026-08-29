from parser import Parseline
import sys
from simualtion import Simulation


class Fly_in:
    """Entry point wrapper for running the Fly-in application.

    The Fly_in class orchestrates parsing the input file and running the
    simulation.
    """

    def run(self) -> None:
        """Parse input and execute the simulation.

        This method constructs a Parseline parser to read the input file and
        then creates and runs the Simulation instance.
        """
        parser = Parseline()
        parser.parse_file()
        simu = Simulation()
        simu.run()


if __name__ == "__main__":
    try:
        launcher = Fly_in()
        launcher.run()
    except BaseException as error:
        print(error, file=sys.stderr)
