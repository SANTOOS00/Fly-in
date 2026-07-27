from typing_extensions import override


class BaseParser:
    def __init__(self, line_str: str) -> None:
        self.line_str: str = line_str

    @override
    def parser(self) -> None:
        pass
