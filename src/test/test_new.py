class Person:
    _instance = None

    def __new__(cls, name):
        if cls._instance is not None:
            raise Exception("Only one object is allowed!")

        cls._instance = super().__new__(cls)
        cls._instance.name = name
        return cls._instance


p1 = Person("mohamed")
print(p1.name)
# p3 = Person()
# p2 = Person()
print("First object created")

# p2 = Person()  # Error