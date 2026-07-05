
# import re


# class Hub:
#     def __init__(self, name: str, y: int, x: int, meta = None
#                  ) -> None:
#         self.name = name
#         self.x = x
#         self.y = y
#         self.meta = meta


# def parse_line_to_object(line: str):
#         """
#         كتآخذ السطر بحال: maze_a1 1 0 [color=blue max_drones=2]
#         وترجع Object مناسب (مثلا Hub)
#         """
#         # print(line)
#         line = line.strip()
#         if not line:
#             return None
#         # print(line)


#         patterns = {
#              r'^(\w+)': True,
#              r'^(\w+)\s+(-?\d+)': True,
#              r'^(\w+)\s+(-?\d+)\s+(-?\d+)(.*)': True,
#         }
#         for key in patterns.keys():
#             match = re.match(key, line)
#             if match is None:
#                  patterns[key] = False
#         print(match)
#         print(patterns)

#         z = match.groups()
#         print(z[3])
#         # print(s)
#         # print(w)
#         # print(a)

#         # print(patterns)
#         # for index, key in enumerate(patterns.keys()):
#         #      print(index)
#         #      if patterns[key]:
#         #           print("valid, in " + str(index))


#         # if match:
#         #     # is_valid_x_and_y(x, y)
#         #     print(options_raw)
#         #     return Hub(name, x, y, options_raw)


# test = "maze_c2 -1 1 [aaa=1]"

# parse_line_to_object(test)

# test_name = {
#     "a": False,
#     "b": True,
#     "c": False
# }

# index = None
# if any(val for index, val in enumerate(test_name.values())):
#     print(f"is ok  {}")

# test_name = {
#     "test5": True,
#     "test4": True,
#     "test3": False,
#     "test2": True,
#     "test1": True,
# }

# if (False or True for check_ru in test_name.values() if check_ru):
#     print("is ok")



# from enum import Enum

# class test_type(Enum):
#     ZONE_ERROR = 0
#     X_ERROR = 1
#     Y_ERROR = 2


# print(test_type(1)) 

for is_not_valid, type_error in enumerate(self._patterns.values(), ErrorLocation):
            if is_not_valid:
                raise ZeroDivisionError(f""  , self.nu_line, ErrorSeverity.Error, ErrorLocation(type_error))