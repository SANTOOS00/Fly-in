import sys
from map_parser import ConfigParser
from graph import Graph


def main() -> None:
    if (len(sys.argv) != 2):
        print("Usage: python3 <name_file>.txt", file=sys.stderr)
        return
    map_parser = ConfigParser()
    graph: Graph = map_parser.parse_pipeline(sys.argv[1])
    # graph = Graph()
    graph.start_connected_zone()
    # print(graph.drones.drones[0]["id"])


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
