import copy

class A:

    def __int__(self):
        self.a = 'a'

    def run(self):
        print("RUN")
    
    def __str__(self):
        return f"{self.a} |"

obj_a = A()

obj_a.a = 'A'

obj_b = copy.deepcopy(obj_a)
obj_b.a = 'SANTOS'

print("obj_a:", obj_a)
print("obj_b:", obj_b)
