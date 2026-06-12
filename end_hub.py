from typing import Dict, Any
from custom_error import ParsingError


class End_hub:
    _instance: "End_hub" = None

    def __new__(cls, name: str, y: int, x: int, meta: Dict[str, Any] = None
                ) -> "End_hub":
        if cls._instance is not None:
            raise ParsingError(
                "Duplicate 'end_hub' defined. Only one start hub is allowed.")

        cls._instance = super().__new__(cls)
        cls._instance.name = name
        cls._instance.y = y
        cls._instance.x = x
        cls._instance.meta = meta
        return cls._instance
