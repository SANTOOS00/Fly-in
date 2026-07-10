from parserconfig import ParserConfig, SafeFileReader
from network import Graph
import sys


def parse_and_print_graph() -> None:
    parser = ParserConfig()
    parser.parse_in_type_line()

    return parser.get_graph


def run_graph(graph: Graph) -> None:
    graph.run()


if __name__ == "__main__":
    try:
        run_graph(parse_and_print_graph())
    except Exception as error:
        print(error, file=sys.stderr)
    finally:
        if SafeFileReader.fd is not None:
            SafeFileReader.fd.close()
