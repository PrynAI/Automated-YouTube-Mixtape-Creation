"""Custom exception hierarchy used by the application."""


class MixtapeError(Exception):
    """Base application error."""


class ValidationError(MixtapeError):
    """Raised when user input or files are invalid."""


class ProcessingError(MixtapeError):
    """Raised when media processing fails."""
