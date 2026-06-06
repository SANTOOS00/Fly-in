from typing import List

class LineValidator:
    def __init__(self, name_file: str) -> None:
        self.name_file = name_file

class Parsing:
    def __init__(self, name_file: str) -> None:
        self.start_hub: Start_hub = None
        self.hub: List[Hub]= []
        self.end_hub: End_hub = None
        self.connection: List = []
        self.git_line: Git_line = Git_line(name_file)

    def parser_args(self) -> None:
        pass
