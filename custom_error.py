from typing import Dict


class FlyinError(Exception):
    """Custom exception type used across the Fly-in project.

    The exception carries a dictionary-style `context` and a class-wide
    line-number counter that can be incremented for error reporting.
    """

    _line_number: int = 0

    def __init__(self, message: str, **context: str) -> None:
        """Create a FlyinError with formatted context.

        Args:
            message: Human-readable error message.
            **context: Arbitrary keyword context providing additional details.
        """
        super().__init__(self.format_message(message, context))
        self.context: Dict[str, str] = context

    def format_message(self,
                       message: str,
                       context: Dict[str, str]
                       ) -> str:
        """Format the message together with the provided context.
        Args:
            message: Base message text.
            context: Mapping of contextual keys/values to include.
        Returns:
            A single string combining message and context for display.
        """
        line_num = context.get("number_line") if context else None
        if line_num is not None:
            return f"\nmessage: {message}\n\nline_number: {line_num}"
        return f"\nmessage: {message}"

    @classmethod
    def add_line_number(cls) -> None:
        """Increment the class-level line-number counter by one."""
        cls._line_number += 1

    @classmethod
    def get_number_line(cls) -> str:
        """Return the current class-level line-number counter value.

        Returns:
            The integer count of lines associated with errors so far.
        """
        return str(cls._line_number)
