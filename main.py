from parserconfig import ParserConfig, SafeFileReader
from network import FlightNetwork, NetworkTopologyBuilder
from network import PathFinder
import sys


def parse() -> None:
    parser = ParserConfig()
    parser.parse_in_type_line()
    return parser.get_network


def run_graph(network: FlightNetwork) -> None:
    print(network.hubs.keys())
    networkbuilder = NetworkTopologyBuilder()
    networkbuilder.populate_network_links(network)
    path_finder = PathFinder()
    path_finder.find_all_paths(networkbuilder.get_network_link(),
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
