from parser import Parseline, FlyinError
from graph import Graph
import sys

class Fly_in:
    @staticmethod
    def run() -> None:
        parser = Parseline()
        parser.parse_file()
        Graph().run()
if __name__ == "__main__":
    try:
        launcher = Fly_in()
        launcher.run()
    except FlyinError as error:
        print(error, file=sys.stderr)







