from parserconfig import ParserConfig, SafeFileReader
import sys


def mainparser() -> None:
    parser = ParserConfig()
    graph = parser.parse_in_type_line()
    for hub in graph.hubs:
        pass
        print(hub.name, hub.meta)
    for conn in graph.connections:
        print(conn.connection, conn)


def maingraph() -> None:
    pass


if __name__ == "__main__":
    try:
        mainparser()
    except Exception as error:
        print(error, file=sys.stderr)
    finally:
        if SafeFileReader.fd is not None:
            SafeFileReader.fd.close()
