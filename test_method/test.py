from typing import Dict

test : Dict[str, int] = {
    "test" : 1,
    "tst" : 1,
    "est" : 1,
    "st" : 1,
    "es " : 1
}

print(isinstance(type(test), Dict))