from typing import List, Dict, Any
from custom_error import FlyinError
import re
from base_parse import BaseParser
from modules import Edge


class MetadataValidator:
    def __init__(self,
                 in_type: BaseParser,
                 data: Dict[str, Any]) -> None:
        self.in_type = in_type
        self.data = data

    @property
    def _get_max_drones(self) -> int:
        try:
            val = int(self.data['max_drones'])
            if val < 0:
                raise FlyinError(
                    "Invalid value for 'max_drones' in metadata: "
                    f"{self.data['max_drones']}",
                    number_line=FlyinError.get_number_line()
                    )
            return val
        except Exception:
            raise FlyinError(
                "Invalid value for 'max_drones' in metadata: "
                f"{self.data['max_drones']}",
                FlyinError.get_number_line(),
            )

    @property
    def get_link_capacity(self) -> int:
        try:
            val = int(self.data['max_link_capacity'])
            if val < 0:
                raise FlyinError(
                    "Invalid value for 'max_link_capacity' in metadata: "
                    f"{self.data['max_link_capacity']}. "
                    "It must be an integer greater than or equal to 1.",
                    FlyinError.get_number_line()
                    )
            return val
        except Exception:
            raise FlyinError(
                "Invalid value for 'max_link_capacity' in metadata: "
                f"{self.data['max_link_capacity']}. "
                "It must be an integer greater than or equal to 1.",
                FlyinError.get_number_line()
            )

    @property
    def _set_max_drones(self) -> None:
        if self.data.get('max_drones'):
            self.data['max_drones'] = self._get_max_drones

    @property
    def _set_max_capacity(self) -> None:
        if self.data.get('max_link_capacity'):
            self.data['max_link_capacity'] = self.get_link_capacity

    def validate_metadata(self) -> Dict[str, Any]:
        self.allowed_status_meta()
        if isinstance(self.in_type, Edge):
            self._set_max_capacity
        else:
            self._set_max_drones
        return (self.data)

    def allowed_status_meta(self) -> None:
        allowed = ["zone", "color", "max_drones"]
        from parser import EdgeParser
        if isinstance(self.in_type, EdgeParser):
            if self.data.get("max_link_capacity") is False:
                raise FlyinError(
                    "Invalid connection metadata\n \n ⚠ Fix: "
                    f"key '{self.data}'"
                    f"allowed \n 'max_link_capacity' just",
                    self.line_number,
                    FlyinError.get_number_line())
        else:
            # print(self.in_type)
            for key in self.data.keys():
                if key not in allowed:
                    raise FlyinError(
                        "Invalid connection metadata\n \n ⚠ "
                        f"Fix: key '{self.data}'"
                        f"\n           allowed       \n'{allowed}'\n "
                        "           just",
                        FlyinError.get_number_line()
                        )


class MetaParser:
    patternsmetadata = {
        r'^\s*\w+=[a-zA-Z0-9]+': False,
        r'^\s*\w+=[a-zA-Z0-9]+(\s+\w+=[a-zA-Z0-9]+)?': False,
        r'^\s*\w+=[a-zA-Z0-9]+(\s+\w+=[a-zA-Z0-9]+)?(\s+\w+=[a-zA-Z0-9]+)?$': False,
        r'^\s*\w+=[a-zA-Z0-9]+(\s+\w+=[a-zA-Z0-9]+)*\s*$': False,
    }

    def __init__(self) -> None:
        self.match: re.Match
        self.typ_obj: BaseParser

    def parse_metadata(self, meta_data: str) -> Dict[str, str] | None:
        meta_data = self._validate_metadata_format(meta_data)
        if len(meta_data) == 0:
            return None
        self._check_syntax_meta(meta_data)

        valid_meta = MetadataValidator(self,
                                       self._split_key_values())
        return (valid_meta.validate_metadata())

    @staticmethod
    def check_duplicates(data: tuple[str]) -> None:
        seen = set()
        for itm in [k.split("=")[0].strip() for k in data]:
            if itm in seen:
                raise FlyinError(f"Duplicate metadata item '{itm}',"
                                          " The first occurrence will "
                                          "be used.",
                                          FlyinError.get_number_line()
                                          )
            else:
                seen.add(itm)

    def _split_key_values(self) -> Dict[str, str]:
        data: str = self.match.group().split()
        MetaParser.check_duplicates(data)
        return (
            {key.lower().strip(): val
                for keyval in data
                for key, val in [keyval.split("=")]}
        )

    def _validate_metadata_format(self, meta_data: str) -> str:
        meta_string = meta_data.strip()
        if not meta_string.startswith("["):
            raise FlyinError("MetaData must start with '['",
                                      FlyinError.get_number_line())
        if not meta_string.endswith("]"):
            raise FlyinError("MetaData missing closing bracket ']'",
                            FlyinError.get_number_line())
        return (meta_string[1:-1].strip())

    def _check_syntax_meta(self, meta_data) -> None:
        for pattern in MetaParser.patternsmetadata:
            match = re.match(pattern, meta_data)
            if match is None:
                MetaParser.patternsmetadata[pattern] = True
            else:
                MetaParser.patternsmetadata[pattern] = False
        self._validate_syntax_meta(meta_data.split())
        self.match = match


    def _validate_syntax_meta(self, data: List[str]) -> None:
        for index, is_not_valid in enumerate(MetaParser.patternsmetadata.
                                             values()):
            if is_not_valid:
                raise FlyinError("Invalid MetaData property syntax at"
                                 f" position {data[index]}. Expected "
                                 "format: ''.",
                                 FlyinError.get_number_line()
                                )
