# from functools import singledispatch
# from typing import Any



# # class A:

# @singledispatch
# def spell(ss, data: Any) -> str:
#     return f'default: {data}{ss}'


# class V:
#     @spell.register(int)
#     def _(self, ss, data) -> str:
#         return f'damage spell: {data}{ss}'


# class S:
#     @spell.register(str)
#     def _(self, ss, data: str) -> str:
#         return f"enchantment: {data}{ss}"


# class B:
#     @spell.register(list)
#     def _(self, ss, data: list) -> str:
#         return f"multi-cast: {data}{ss}"


# print(spell("22", 22))
# from enum import Enum

# class Type_Error(Enum):
#     Warning = "Warning"
#     Error = "Error"


# class ParsingError(Exception):
#     def __init__(self, message: str, number_line: int, type_error: Type_Error) -> None:
#         self.message = message
#         self.number_line = number_line
#         self.type_error = type_error
        

#     def _get_error(self) -> str:
#         return f"[{self.type_error.value}] line {self.number_line}: {self.message}"


# if __name__ == "__main__":
#     try:
#         raise ParsingError("test error", 2, Type_Error.Warning)
#     except Exception as error:
#         print(error._get_error())

# from pathlib import Path

# file_path = Path("../main.py")

# if file_path.exists():
#     print("File exists")
# else:
#     print("Not found")



# from pathlib import Path
# import os

# path = Path("../ain.py")

# if path.exists:
#     print("is ok")

# if os.access(path, os.R_OK):
#     print("you can read")

test2 = "# test tprint(text.split(sep=, maxsplit=2))"
test1 = "test tprint(text.split#(sep="

print(test1.split("#", maxsplit=1)[0])
# print(test2.split("#", maxsplit=1))