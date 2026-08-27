import sys

try:
    import webcolors    # type: ignore[import-untyped, unused-ignore]
    from rich.console import Console
except ModuleNotFoundError as e:
    print(f"\nMissing module: {e}", file=sys.stderr)
    print("Solution: run the command 'make install'\n", file=sys.stderr)
    exit()


class Color:
    """Build and print Rich-formatted colored output.

    The Color helper accumulates pieces of text in an internal buffer and
    prints them using Rich's Console. It can also wrap strings in color
    markup using webcolors name-to-hex mapping with a safe fallback.
    """

    def __init__(self) -> None:
        """Initialize an empty output buffer and a Rich Console."""
        self.output = ''
        self.console = Console()

    def add(self, string: str) -> None:
        """Append text to the internal output buffer.

        Args:
            string: Text to append to the buffer.
        """
        self.output += string

    def print_string(self) -> None:
        """Print the current buffer contents to the terminal via Rich."""
        self.console.print(self.output)

    def join_color_string(self, string: str, color: str) -> str | None:
        """Return the given text wrapped in Rich color markup.

        Args:
            string: Text to format.
            color: Named CSS color to apply. If the name is invalid, a
                fallback hex color is used.

        Returns:
            A Rich-style formatted string like "[#RRGGBB]text[/]".
        """
        try:
            color_hex = webcolors.name_to_hex(color)
        except ValueError:
            color_hex = '#0B192C'
        return f'[{color_hex}]{string}[/]'

    def clear(self) -> None:
        """Clear the internal output buffer."""
        self.output = ''
