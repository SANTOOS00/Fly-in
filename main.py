from parser import Parseline, FlyinError


class Fly_in:
    @staticmethod
    def run() -> None:
        parser = Parseline()
        parser.parse_file()

if __name__ == "__main__":
    try:
        launcher = Fly_in()
        launcher.run()
    except FlyinError as error:
        error.report()







