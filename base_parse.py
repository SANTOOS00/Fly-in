from abc import ABC, abstractmethod
from typing import Any


class BaseParser(ABC):
    def __init__(self, line_str: str) -> None:
        """Initializes the FlyinError exception
            Args:
                line_str (str) = 
        """
        self.line_str: str = line_str

    @abstractmethod
    def parser(self) -> Any:
        pass
