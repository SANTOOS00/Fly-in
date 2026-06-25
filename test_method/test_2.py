from functools import singledispatch
from typing import Any



# class A:

@singledispatch
def spell(ss, data: Any) -> str:
    return f'default: {data}{ss}'


class V:
    @spell.register(int)
    def _(self, ss, data) -> str:
        return f'damage spell: {data}{ss}'


class S:
    @spell.register(str)
    def _(self, ss, data: str) -> str:
        return f"enchantment: {data}{ss}"


class B:
    @spell.register(list)
    def _(self, ss, data: list) -> str:
        return f"multi-cast: {data}{ss}"


print(spell("22", 22))
