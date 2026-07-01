"""Logging configuration for EduTrack Pro."""

import logging


def configure_logging() -> None:
    """Configure application logging with a concise production-safe format."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    """Return a named logger."""

    return logging.getLogger(name)
