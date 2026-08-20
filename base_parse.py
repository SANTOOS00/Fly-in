from abc import ABC, abstractmethod


class BaseParser(ABC):
    def __init__(self, line_str: str) -> None:
        self.line_str: str = line_str

    @abstractmethod
    def parser(self) -> None:
        pass
