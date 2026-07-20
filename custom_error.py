from typing import Dict, Callable, Any

class   FlyinError(Exception):
    line_number: int = 1

    def __init__(self, message: str, **context) -> None:
        super().__init__(message)
        self.context: Dict[str, str] = context


    @classmethod
    def add_line_number(cls: 'FlyinError') -> None:
        cls.line_number += 1
    
    @classmethod
    def get_number_line(cls: 'FlyinError') -> str:
        return str(cls.line_number)

    
    def __add__(self, other: Dict[str, str]) -> 'FlyinError':
        self.context.update(other)
        return self 
    
    def report(self) -> str:
        print(self.context)     
        print(self)

    def check_error(type_error: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs) -> Any:
                try:
                    func(*args, **kwargs)
                except FlyinError as error:
                    raise FlyinError(str(error),
                                    type_error=type_error,
                                    ) + error.context
            return wrapper
        return decorator





# from enum import Enum


# class ErrorSeverity(Enum):
#     Warning = "Warning"
#     Error = "Error"


# class ErrorLocation(Enum):
#     ZONE = "Zone name is not valid"
#     X_AXIS = "X coordinate is not valid"
#     Y_AXIS = "Y coordinate is not valid"


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


