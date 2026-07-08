# from dataclasses import dataclass, field
# from typing import List

# # اللائحة اللي كتحديد القيم المسموحة
# ALLOWED_VALUES = ['test1', 'test2', 'test3', 'test4', 'test5']

# @dataclass
# class MyClass:
#     # القيمة الافتراضية
#     my_field: str

#     def __post_init__(self):
#         print("ss")
#         # التحقق: واش القيمة موجودة فـ اللائحة؟
#         if self.my_field not in ALLOWED_VALUES:
#             raise ValueError(f"القيمة '{self.my_field}' غير مسموحة. القيم المسموحة هي: {ALLOWED_VALUES}")

# # تجربة صحيحة
# obj1 = MyClass('test2') 
# print(obj1.my_field) # Output: test2

# # تجربة خاطئة (غادي تعطي خطأ)
# try:
#     obj2 = MyClass('test99') 
# except ValueError as e:
#     print(f"خطأ: {e}")   
# seen = set()

# data = ["test 1", "test 2", "test 3"]
# for itm in [k.split("=")[0].strip() for k in data]:
#     print(itm)

import re

tet = "final_merge-final_tortur- -[e1kdqendned]"
patterns = {
        r'^(\w+)': False,
        r'^(\w+)-(\w+)': False,
        r'^(\w+)-(\w+)(.*)': False
    }


e = re.match(r'^(\w+)', tet)
if e is None:
    print("not valid")
else:
    print(e.groups())
