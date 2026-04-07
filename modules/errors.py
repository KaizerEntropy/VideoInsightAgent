class VideoInsightError(Exception):
    """Base exception for recoverable project errors."""


class ConfigurationError(VideoInsightError):
    """Raised when required configuration is missing or invalid."""


class ExternalServiceError(VideoInsightError):
    """Raised when an external API or model invocation fails."""


class ProcessingError(VideoInsightError):
    """Raised when a local processing step cannot be completed."""
