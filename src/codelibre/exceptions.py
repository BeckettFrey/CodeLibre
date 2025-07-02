# src/codelibre/exceptions.py
class ExitRequestedException(Exception):
    """Raised when user requests to exit."""
    def __init__(self, message="Exit requested by user"):
        super().__init__(message)


class SanitizationError(Exception):
    """Raised if a commit message fails sanitization."""
    def __init__(self, message="Commit message failed sanitization"):
        super().__init__(message)


class TruncationException(Exception):
    """Raised if chat context exceeds maximum allowed length."""
    def __init__(self, message="Chat context exceeds maximum allowed length"):
        super().__init__(message)


class CodeLibreEnvironmentError(Exception):
    """Raised if required environment variables are missing."""
    def __init__(self, message="Required environment variable is missing"):
        super().__init__(message)

class GitCommandError(Exception):
    """Raised if a Git command fails."""
    def __init__(self, message="Git command failed"):
        super().__init__(message)