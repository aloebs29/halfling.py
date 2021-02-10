class HalflingError(Exception):
    """Encapsulates all exceptions risen by halfling."""


class HalflingCompileError(HalflingError):
    """Encapsulates all compile errors."""


class HalflingLinkError(HalflingError):
    """Encapsulates all link errors."""
