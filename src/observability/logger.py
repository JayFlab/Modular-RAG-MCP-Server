"""
Observability logger module.

Provides stderr-based logging for the application.
JSON Lines structured logging will be added in Phase F.
"""
import logging
import sys


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Get a configured logger that outputs to stderr.

    Args:
        name: Logger name (typically __name__).
        level: Logging level (default: INFO).

    Returns:
        Configured logging.Logger instance.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)

    return logger
