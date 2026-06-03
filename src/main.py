import sys
from parser import Parsing


def main() -> None:
    if (len(sys.argv) != 2):
        print("Usage: python3 <name_file>.txt", file=sys.stderr)
        return
    Parsing.parser_args(sys.argv[1])


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
