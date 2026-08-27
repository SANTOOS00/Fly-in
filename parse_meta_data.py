from typing import List, Dict, Any
from custom_error import FlyinError
import re


class MetadataValidator:
    """Validate and coerce metadata key/value mappings for hubs and edges.

    The validator receives the parser class name (in_type) to distinguish
    edge-specific rules from hub metadata validation.
    """
    def __init__(self,
                 in_type: str,
                 data: Dict[str, Any]) -> None:
        self.in_type = in_type
        self.data = data

    @property
    def _get_max_drones(self) -> int:
        """Return a validated integer for 'max_drones' from metadata.

        Raises:
            FlyinError: When parsing fails or the value is negative.
        """
        try:
            val = int(self.data['max_drones'])
            if val < 0:
                raise FlyinError(
                    "Invalid value for 'max_drones' in metadata: "
                    f"{self.data['max_drones']}",
                    number_line=str(FlyinError.get_number_line())
                    )
            return val
        except Exception:
            raise FlyinError(
                "Invalid value for 'max_drones' in metadata: "
                f"{self.data['max_drones']}",
                number_line=str(FlyinError.get_number_line())
            )

    @property
    def get_link_capacity(self) -> int:
        """Return a validated integer for 'max_link_capacity' from metadata.

        Raises:
            FlyinError: When parsing fails or the value is negative.
        """
        try:
            val = int(self.data['max_link_capacity'])
            if val < 0:
                raise FlyinError(
                    "Invalid value for 'max_link_capacity' in metadata: "
                    f"{self.data['max_link_capacity']}. "
                    "It must be an integer greater than or equal to 1.",
                    number_line=str(FlyinError.get_number_line())
                    )
            return val
        except Exception:
            raise FlyinError(
                "Invalid value for 'max_link_capacity' in metadata: "
                f"{self.data['max_link_capacity']}. "
                "It must be an integer greater than or equal to 1.",
                number_line=str(FlyinError.get_number_line())
            )

    @property
    def _set_max_drones(self) -> None:
        """Coerce 'max_drones' to an int in the underlying data mapping."""
        if self.data.get('max_drones'):
            self.data['max_drones'] = self._get_max_drones

    @property
    def _set_max_capacity(self) -> None:
        """Coerce 'max_link_capacity' to an int in the
        underlying data mapping."""
        if self.data.get('max_link_capacity'):
            self.data['max_link_capacity'] = self.get_link_capacity

    def validate_metadata(self) -> Dict[str, Any]:
        """Run overall metadata validation and coercion.

        Returns:
            The possibly-modified data mapping with corrected integer types.
        """
        self.allowed_status_meta()
        if self.in_type == "EdgeParser":
            self._set_max_capacity
        else:
            self._set_max_drones
        return self.data

    def allowed_status_meta(self) -> None:
        """Ensure only allowed metadata keys are present for the parser type.

        Raises:
            FlyinError: When unexpected keys or invalid edge
            metadata are found.
        """
        allowed = ["zone", "color", "max_drones"]
        if self.in_type == "EdgeParser":
            if self.data.get("max_link_capacity") is False:
                raise FlyinError(
                    "Invalid connection metadata\n \n ⚠ Fix: "
                    f"key '{self.data}'"
                    f"allowed \n 'max_link_capacity' just",
                    number_line=str(FlyinError.get_number_line()))
        else:
            for key in self.data.keys():
                if key not in allowed:
                    raise FlyinError(
                        "Invalid connection metadata\n \n ⚠ "
                        f"Fix: key '{self.data}'"
                        f"\n           allowed       \n'{allowed}'\n "
                        "           just",
                        number_line=str(FlyinError.get_number_line())
                        )


class MetaParser:
    """Mixin providing metadata parsing utilities used by line parsers."""
    patternsmetadata = {
        r'^\s*\w+=[a-zA-Z0-9]+':
        False,
        r'^\s*\w+=[a-zA-Z0-9]+(\s+\w+=[a-zA-Z0-9]+)?':
        False,
        r'^\s*\w+=[a-zA-Z0-9]+(\s+\w+=[a-zA-Z0-9]+)?(\s+\w+=[a-zA-Z0-9]+)?$':
        False,
        r'^\s*\w+=[a-zA-Z0-9]+(\s+\w+=[a-zA-Z0-9]+)*\s*$':
        False,
    }

    def parse_metadata(self, meta_data: str) -> Dict[str, str] | None:
        """Parse a bracketed metadata string into a dictionary.

        Args:
            meta_data: The raw metadata text, including surrounding brackets.

        Returns:
            A dictionary of key->value strings, or None when empty.
        """
        meta_data = self._validate_metadata_format(meta_data)
        if len(meta_data) == 0:
            return None
        self._check_syntax_meta(meta_data)

        valid_meta: MetadataValidator = \
            MetadataValidator(type(self).__name__, self._split_key_values())
        return (valid_meta.validate_metadata())

    @staticmethod
    def check_duplicates(data: list[Any]) -> None:
        """Raise FlyinError when duplicate metadata keys appear."""
        seen = set()
        for itm in [k.split("=")[0].strip() for k in data]:
            if itm in seen:
                raise FlyinError(f"Duplicate metadata item '{itm}',"
                                 " The first occurrence will "
                                 "be used.",
                                 number_line=str(FlyinError.get_number_line()))
            else:
                seen.add(itm)

    def _split_key_values(self) -> Dict[str, Any]:
        """Split a regex match group into a dict of
        lower-cased key/value pairs.

        Returns:
            Mapping of metadata keys to their string values.
        """
        data: List[str] = self.match.group().split()
        MetaParser.check_duplicates(data)
        return (
            {key.lower().strip(): val
                for keyval in data
                for key, val in [keyval.split("=")]}
        )

    def _validate_metadata_format(self, meta_data: str) -> str:
        """Validate surrounding brackets and return inner metadata string.

        Args:
            meta_data: Raw metadata including surrounding brackets.

        Returns:
            Inner metadata string without surrounding '[' and ']'.

        Raises:
            FlyinError: When metadata does not start with '[' or end with ']'.
        """
        meta_string = meta_data.strip()
        if not meta_string.startswith("["):
            raise FlyinError("MetaData must start with '[",
                             number_line=str(FlyinError.get_number_line()))
        if not meta_string.endswith("]"):
            raise FlyinError("MetaData missing closing bracket ']'",
                             number_line=str(FlyinError.get_number_line()))
        return (meta_string[1:-1].strip())

    def _check_syntax_meta(self, meta_data: str) -> None:
        for pattern in MetaParser.patternsmetadata:
            match: re.Match[str] | None = re.match(pattern, meta_data)
            if match is None:
                MetaParser.patternsmetadata[pattern] = True
            else:
                MetaParser.patternsmetadata[pattern] = False
        self._validate_syntax_meta(meta_data.split())
        if match is None:
            return None
        self.match = match

    def _validate_syntax_meta(self, data: List[str]) -> None:
        for index, is_not_valid in enumerate(MetaParser.patternsmetadata.
                                             values()):
            if is_not_valid:
                raise FlyinError("Invalid MetaData property syntax at"
                                 f" position {data[index - 1]}. Expected "
                                 "format: ",
                                 number_line=str(FlyinError.get_number_line()))
