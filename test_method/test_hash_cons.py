class A:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age


    def __hash__(self):
        print('test hash is ok')
        return hash(self.name)

    def __del__(self) -> None:
        print("test del is ok")


test_1 = A('haimid', 12)
test_2 = A('haimid', 12)
test_3 = A('haimid', 12)
print(test_1 == test_2)