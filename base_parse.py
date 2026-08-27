from abc import ABC, abstractmethod
from typing import Any


class BaseParser(ABC):
    """Abstract base parser that stores a single input line.

    Subclasses should implement the `parser` method to parse the provided
    `line_str` into the desired structured representation.
    """

    def __init__(self, line_str: str) -> None:
        """Initialize the parser with the raw input line.

        Args:
            line_str: The raw string line to parse.
        """
        self.line_str: str = line_str

    @abstractmethod
    def parser(self) -> Any:
        """Parse the stored line and return a structured representation.

        Returns:
            Parsed value(s). Concrete return type depends on the
            implementation in subclasses.
        """
        pass
