
import re


class Hub:
    def __init__(self, name: str, y: int, x: int, meta: any = None
                 ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.meta = meta


def parse_line_to_object(line: str):
        """
        كتآخذ السطر بحال: maze_a1 1 0 [color=blue max_drones=2]
        وترجع Object مناسب (مثلا Hub)
        """
        print(line)
        line = line.strip()
        if not line:
            return None
        print(line)

        pattern = r'^(\w+)\s+(\d+)\s+(\d+)(\s+)(\[\w+\=\w+\])$'
        
        match = re.match(pattern, line)
        print(match )

        if match:
            name, x, y, options_raw = match.groups()
            # is_valid_x_and_y(x, y)
            print(options_raw)
            return Hub(name, x, y, options_raw)


test = "maze_c2 3 2     [[]"

print(parse_line_to_object(test).meta)