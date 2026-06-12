import sys
from map_parser import ConfigParser


def main() -> None:
    if (len(sys.argv) != 2):
        print("Usage: python3 <name_file>.txt", file=sys.stderr)
        return
    map_parser = ConfigParser(sys.argv[1])
    map_parser.parse_pipeline()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
