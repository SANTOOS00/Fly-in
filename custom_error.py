from typing import Dict, Callable, Any

class   FlyinError(Exception):
    _line_number: int = 0

    def __init__(self, *message: str, **context) -> None:
        super().__init__(self.format_message(context, message))
        self.context: Dict[str, str] = context

    def format_message(self, context: str, message: str) -> str:
        return f"{message} {context}"

    @classmethod
    def add_line_number(cls) -> None:
        cls._line_number += 1
    
    @classmethod
    def get_number_line(cls) -> str:
        return str(cls._line_number)
