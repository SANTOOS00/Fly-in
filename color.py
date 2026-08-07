from rich import Console
from webcolors import name_to_hex


console = Console(force_terminal=True, color_system="truecolor")

class Color:
    def __init__(self) -> None:
        self.output = ''
        self.console = Console(force_terminal=True, color_system="truecolor")

    def append_string_outout(self, string: str) -> None:
        self.string_output += string

    def print_string(self) -> None:
        self.console.print(self.output)

    @staticmethod
    def switch_stron_in_hex(string: str) -> str:
        return name_to_hex(string)

    def join_color_string(self, string: str, color: str) -> str:
        color_hex = self.switch_stron_in_hex(color)
        return f'[{color_hex}]{string}[/]'

    def clear(self) -> None:
        self.string_output = ''


color = Color()

color.append_string_outout(f'd1 {color.join_color_string('ssssss','red')}')
color.print_string()



from rich import print

class ColorBuilder:
    def __init__(self) -> None:
        self.output = ""

    def add(self, text: str, color: str | None = None) -> "ColorBuilder":
        """تضيف نص، مع لون اختياري"""
        if color:
            self.output += f"[{color}]{text}[/]"
        else:
            self.output += text
        return self  # باش تقدر تدير .add().add() ف نفس السطر

    def print(self) -> None:
        """طبع النص المجمع"""
        print(self.output)

    def clear(self) -> None:
        """تمسح النص المجمع"""
        self.output = ""


# 🚀 طريقة الاستعمال (سهلة بزاف):
cb = ColorBuilder()

# تقدر تضيف بالسطر بالسطر:
cb.add("d1 ")
cb.add("ssssss", color="red")
cb.add(" - ok!", color="bold green")
cb.print()

# أو تجمعهم كاملين ف سطر واحد:
cb.clear()
cb.add("d1 ").add("ssssss", "red").add(" - ok!", "bold green").print()