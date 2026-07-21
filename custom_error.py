from typing import Dict, Callable, Any

class   FlyinError(Exception):
    _line_number: int = 0

    def __init__(self, *message: str, **context) -> None:
        super().__init__(self.format_message(context, message))
        self.context: Dict[str, str] = context

    def format_message(self, context, message) -> str:
        return f"{message} {context}"

    @classmethod
    def add_line_number(cls: 'FlyinError') -> None:
        cls._line_number += 1
    
    @classmethod
    def get_number_line(cls: 'FlyinError') -> str:
        return str(cls._line_number)



# class BaseError(Exception):
#     """
#     #|------------------------------------------------------------------|
#     #|            ----- custom errors in project ------                 |
#     #|------------------------------------------------------------------|
#     """

#     def __init__(self, message: str, line_number: int | None = None,
#                  severity: ErrorSeverity | None = None) -> None:
#         super().__init__(message)
#         self.message = message
#         self.line_number = line_number
#         self.severity = severity

#     def __str__(self) -> str:
#         return (
#             f"[{self.severity.value}] line {self.line_number}: "
#             f"{self.message}")


# class PathError(BaseError):
#     def __init__(self, message: str, severity: ErrorSeverity | None = None
#                  ) -> None:
#         super().__init__(message, severity=severity)

#     def __str__(self) -> str:
#         return f"[{self.severity.value}]: {self.message}"


# class HubError(BaseError):
#     def __init__(self, message: str, line_number: int, severity: ErrorSeverity
#                  ) -> None:
#         super().__init__(message, line_number, severity)

#     def __str__(self) -> str:
#         return (
#                 f"\n[{self.severity.value}] Line {self.line_number}\n"
#                 f"  ➜ Input : {self.message}\n"
#             )


# class ConnectionError(BaseError):
#     def __init__(self, message: str, line_number: int,
#                  severity: ErrorSeverity) -> None:
#         super().__init__(message, line_number, severity)

#     def __str__(self):
#         return (
#                 f"\n[{self.severity.value}] Line {self.line_number}\n"
#                 f"  ➜ Input : {self.message}\n"
#         )


# class UtilsError(BaseError):
#     def __init__(self, message: str, line_number: int | None = None,
#                  severity: ErrorSeverity | None = None) -> None:
#         super().__init__(message, line_number, severity)

#     def __str___(self):
#         return (
#                 f"\n[{self.severity.value}] Line {self.line_number}\n"
#                 f"  ➜ Input : {self.message}\n"
#             )


# class ZoneWithCoordsParserError(BaseError):
#     def __init__(self,
#                  message: str,
#                  line_number: int | None = None,
#                  severity: ErrorSeverity | None = None,
#                  location: ErrorLocation | None = None) -> None:
#         super().__init__(message, line_number, severity)
#         self.location = location

#     def __str__(self) -> None:
#         if self.location == ErrorLocation.ZONE:
#             return (
#                 f"\n[{self.severity.value}] Line {self.line_number}"
#                 f" at {self.location.value}:\n"
#                 f"  ➜ Input : {self.message}\n"
#                 f"  ⚠  Fix: {self.severity.value} ⚠  Fix: Error: Invalid zone "
#                 "format. The zone name may contain any characters "
#                 "except spaces and hyphens ('-')..\n"
#             )
#         else:
#             return (
#                 f"\n[{self.severity.value}] Line {self.line_number}"
#                 f" at {self.location.value}:\n"
#                 f"  ➜ Input : {self.message}\n"
#                 f"  ⚠  Fix: {self.severity.value} coordinates must be integers"
#                 " or negative numbers only.\n"
#             )


# class MetaDataParserError(BaseError):
#     def __init__(self, message: str, line_number: int, location: ErrorLocation
#                  ) -> None:
#         super().__init__(message, line_number, location)

#     def __str__(self) -> str:
#         return (f"\n[{self.severity.value}] Line {self.line_number}\n"
#                 f"  ➜ Input : {self.message}\n")


