"""Custom exceptions."""


class HalflingError(Exception):
    """Encapsulates exceptions risen by halfling."""


class HalflingCompileError(HalflingError):
    """Encapsulates compile errors."""


class HalflingLinkError(HalflingError):
    """Encapsulates link errors."""
