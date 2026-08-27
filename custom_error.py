from typing import Dict


class FlyinError(Exception):

    _line_number: int = 0

    def __init__(self, message: str, **context: str) -> None:
        super().__init__(self.format_message(message, context))
        self.context: Dict[str, str] = context

    def format_message(
        self,
        message: str,
        context: Dict[str, str]
    ) -> str:
        return f"{message} {context}"

    @classmethod
    def add_line_number(cls) -> None:
        cls._line_number += 1

    @classmethod
    def get_number_line(cls) -> int:
        return cls._line_number
