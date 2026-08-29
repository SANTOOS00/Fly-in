from typing import List, Dict, Any
from custom_error import FlyinError
import re
import json
from pathlib import Path


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
                    "[ERROR]: Invalid value for 'max_drones' in metadata: "
                    f"{self.data['max_drones']}",
                    number_line=FlyinError.get_number_line()
                    )
            return val
        except Exception:
            raise FlyinError(
                "[ERROR]: Invalid value for 'max_drones' in metadata: "
                f"{self.data['max_drones']}",
                number_line=FlyinError.get_number_line()
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
                    "[ERROR]: Invalid value for 'max_link_capacity'"
                    f" in metadata: {self.data['max_link_capacity']}. "
                    "It must be an integer greater than or equal to 1.",
                    number_line=FlyinError.get_number_line()
                    )
            return val
        except Exception:
            raise FlyinError(
                "[ERROR]: Invalid value for 'max_link_capacity' in metadata: "
                f"{self.data['max_link_capacity']}. "
                "It must be an integer greater than or equal to 1.",
                number_line=FlyinError.get_number_line()
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
                    "[ERROR]: Invalid connection metadata ⚠ Fix: "
                    f"key '{self.data}'"
                    f"allowed 'max_link_capacity' just",
                    number_line=FlyinError.get_number_line())
        else:
            for key in self.data.keys():
                if key not in allowed:
                    raise FlyinError(
                        "[ERROR]: Invalid connection metadata ⚠ "
                        f"Fix: key '{self.data} allowed '{allowed}' "
                        "just",
                        number_line=FlyinError.get_number_line()
                        )


class MetaParser:
    """Mixin providing metadata parsing utilities used by line parsers."""

    def __init__(self) -> None:
        """Initialize the parser state."""
        self.match: re.Match

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
                raise FlyinError(f"[ERROR]: Duplicate metadata item '{itm}',"
                                 " The first occurrence will "
                                 "be used.",
                                 number_line=FlyinError.get_number_line())
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
            raise FlyinError("[ERROR]: MetaData must start with '[",
                             number_line=FlyinError.get_number_line())
        if not meta_string.endswith("]"):
            raise FlyinError("[ERROR]: MetaData missing closing bracket ']'",
                             number_line=FlyinError.get_number_line())
        return (meta_string[1:-1].strip())

    def _check_syntax_meta(self, meta_data: str) -> None:
        """Check metadata syntax against known patterns."""
        patterns = self.__get_patternmetadata()
        list_action = []
        for pattern in patterns.values():
            match: re.Match[str] | None = re.match(pattern, meta_data)
            if match is None:
                list_action.append(True)
            else:
                list_action.append(False)

        self._validate_syntax_meta(list_action, meta_data.split())
        if match is None:
            return None
        self.match = match

    def __get_patternmetadata(self) -> Dict[re.Match, bool]:
        """Load the metadata validation patterns from the project JSON file."""
        path_pattern = Path('patternsmetadata.json')
        if not path_pattern.exists():
            raise FlyinError( "The 'patternsmetadata.json' file is missing. "
                              "Please make sure it is downloaded"
                              " from the project repository.")
        with open(path_pattern, 'r') as fd:
            patterns = json.load(fd)
        return patterns

    def _validate_syntax_meta(self, list_action, data: List[str]) -> None:
        """Raise an error when metadata does not match the expected syntax."""
        for is_not_valid in list_action:
            if is_not_valid:
                raise FlyinError("[ERROR]: Invalid metadata property syntax at"
                                 f" position  '{data}'. Expected format: "
                                 "key=value. For hubs, valid properties are: "
                                 "Hub: color=name_string, zone=[normal ,"
                                 "priority ,restricted, blocked"
                                 " max_drones=integer. "
                                 "For connections: max_link_capacity=integer.",
                                 number_line=FlyinError.get_number_line())
