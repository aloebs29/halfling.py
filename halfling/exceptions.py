"""Custom exceptions."""


class HalflingError(Exception):
    """Encapsulates exceptions risen by halfling."""


class HalflingSyntaxError(HalflingError):
    """Encapsulates syntax errors encountered in the halfling extension file."""


class HalflingCompileError(HalflingError):
    """Encapsulates compile errors."""


class HalflingLinkError(HalflingError):
    """Encapsulates link errors."""
