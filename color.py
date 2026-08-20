import sys

try:
    import webcolors
    from rich.console import Console
except ModuleNotFoundError as e:
    print(f"\nMissing module: {e}", file=sys.stderr)
    print("Solution: run the command 'make install'\n", file=sys.stderr)
    exit()


class Color:
    def __init__(self) -> None:
        self.output = ''
        self.console = Console()

    def add(self, string: str) -> None:
        self.output += string

    def print_string(self) -> None:
        self.console.print(self.output)

    def join_color_string(self, string: str, color: str) -> str | None:
        try:
            color_hex = webcolors.name_to_hex(color)
        except ValueError:
            color_hex = '#0B192C'
        return f'[{color_hex}]{string}[/]'

    def clear(self) -> None:
        self.output = ''
