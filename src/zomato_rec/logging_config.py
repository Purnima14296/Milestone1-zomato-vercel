from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler


def configure_logging(level: str = "INFO") -> None:
    """
    Configure console + file logging.

    Logs are written to `logs/app.log` with rotation.
    """

    log_level = getattr(logging, level.upper(), logging.INFO)

    os.makedirs("logs", exist_ok=True)

    root = logging.getLogger()
    root.setLevel(log_level)

    # Avoid duplicate handlers if configure_logging is called multiple times.
    if root.handlers:
        return

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler()
    console.setLevel(log_level)
    console.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        filename=os.path.join("logs", "app.log"),
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    root.addHandler(console)
    root.addHandler(file_handler)

