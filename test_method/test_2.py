from typing import Any, Callable, Dict

class ErrorFlyIn(Exception):
    def __init__(self, message: str, **context: str) -> None:
        super().__init__(message)
        self.context: Dict[str, str] = context

    def __add__(self, other: Dict[str, str]) -> "ErrorFlyIn":
        print(self.context)
        self.context.update(other)
        return self

    def str_with_context(self) -> str:
        print(self.context)
        print(self)

    @staticmethod
    def spread(title: str, ww: int) -> Callable:
        def decorator(func: Callable) -> Callable:
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    return func(*args, **kwargs)
                except ErrorFlyIn as e:
                    print(str(e))
                    raise ErrorFlyIn(str(e),ww=ww,  title=title) + e.context
                except Exception as e:
                    raise ErrorFlyIn(str(e), title=title)
            return wrapper
        return decorator



@ErrorFlyIn.spread(title="3amal / ", ww=12)
def divide(a: int, b: int):
    return a / b

@ErrorFlyIn.spread(title="hamid 5wrni", ww=122)
def calculate_unit_price(total_price: int, quantity: int):
    if quantity == 0:
        raise ErrorFlyIn("test cal 1", file="app.py", line="5")
@ErrorFlyIn.spread(title="queue == 0", ww=13)
def calculate_unit(total_price: int, quantity: int):
    if quantity == 0:
        raise ErrorFlyIn("test cal 2", file="app.py", line="45")
    
    return divide(total_price, quantity)


try:
    calculate_unit_price(100, 0)
    calculate_unit(100, 0)

except ErrorFlyIn as e:
    print("--- تم التقاط خطأ (Error Caught) ---")
    print(e.str_with_context())