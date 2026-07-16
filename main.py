from parserconfig import ParserConfig, SafeFileReader
from network import FlightNetwork, NetworkTopologyBuilder
from network import PathFinder
import sys


def parse() -> None:
    parser = ParserConfig()
    parser.parse_in_type_line()
    return parser.get_network


def run_graph(network: FlightNetwork) -> None:
    networkbuilder = NetworkTopologyBuilder()
    networkbuilder.populate_network_links(network)
    path_finder = PathFinder(network)
    path_finder.Dijkstra(networkbuilder.get_graph(),
                               network.get_start(),
                               network.get_end())

if __name__ == "__main__":
    try:
        run_graph(parse())
    except Exception as error:
        print(error, file=sys.stderr)
    finally:
        if SafeFileReader.fd is not None:
            SafeFileReader.fd.close()
