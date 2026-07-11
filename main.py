from parserconfig import ParserConfig, SafeFileReader
from network import FlightNetwork, NetworkTopologyBuilder
import sys


def parse() -> None:
    parser = ParserConfig()
    parser.parse_in_type_line()
    return parser.get_network


def run_graph(network: FlightNetwork) -> None:
    networkbuilder = NetworkTopologyBuilder()
    networkbuilder.build(network)


if __name__ == "__main__":
    try:
        run_graph(parse())
    except Exception as error:
        print(error, file=sys.stderr)
    finally:
        if SafeFileReader.fd is not None:
            SafeFileReader.fd.close()
