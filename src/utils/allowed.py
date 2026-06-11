from parser.custom_error import ParsingError


def allowed_status(status_zone: str) -> str:
    allowed = ["normal", "blocked", "restricted", "priority"]
    status = status_zone.lower()
    if status not in allowed:
        raise ParsingError(
            f"Invalid status_zone '{status}'. "
            f"Allowed values: {', '.join(allowed)}"
        )
    return status
