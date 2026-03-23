"""Logging setup for Softkillbot."""

import logging
import json
from datetime import datetime
from pythonjsonlogger import jsonlogger
from .config import get_settings


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with additional fields."""

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["timestamp"] = datetime.utcnow().isoformat()
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        log_record["module"] = record.module


def setup_logging() -> logging.Logger:
    """Configure logging for the application."""
    settings = get_settings()
    
    # Create logger
    logger = logging.getLogger("softkillbot")
    logger.setLevel(getattr(logging, settings.log_level))

    # Console handler with JSON formatter
    console_handler = logging.StreamHandler()
    json_formatter = CustomJsonFormatter()
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)

    # File handler for errors
    try:
        file_handler = logging.FileHandler("logs/softkillbot.log")
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(json_formatter)
        logger.addHandler(file_handler)
    except (FileNotFoundError, OSError):
        logger.warning("Could not create logs directory")

    return logger


# Initialize logger
logger = setup_logging()
