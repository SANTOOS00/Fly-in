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
