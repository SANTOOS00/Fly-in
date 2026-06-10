from parser.custom_error import ParsingError


def allowed_status(status_zone: str, line: int) -> str:
    allowed = ["normal", "blocked", "restricted", "priority"]
    status = status_zone.lower()
    if status not in allowed:
        raise ParsingError(
            f"Line {line}: Invalid status_zone '{status}'. "
            f"Allowed values: {', '.join(allowed)}"
        )
    return status
