import logging
import logging.config
from pathlib import Path
import sys

# Create a logs directory if it doesn't exist
log_dir = Path("../logs")
log_dir.mkdir(exist_ok=True)

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # Keep other loggers intact
    "formatters": {
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "simple": {
            "format": "%(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "stream": sys.stdout,
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": log_dir / "app.log",
            "level": "INFO",
            "formatter": "detailed",
            "encoding": "utf-8"
        },
        "error_file": {
            "class": "logging.FileHandler",
            "filename": log_dir / "errors.log",
            "level": "ERROR",
            "formatter": "detailed",
            "encoding": "utf-8"
        },
    },
    "root": {  # Root logger for all modules
        "level": "DEBUG",
        "handlers": ["console", "file", "error_file"],
    }
}

def setup_logging():
    """Initialize logging configuration for the entire application."""
    logging.config.dictConfig(LOG_CONFIG)
