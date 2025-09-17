# app/logger.py
import logging
from flask import Flask

def setup_logging(app: Flask, level=logging.INFO):
    """
    Setup structured JSON-like logging for the Flask app.
    Logs to stdout with time, level, and message in JSON format.

    Args:
        app (Flask): Flask application instance
        level (int): Logging level (default: logging.INFO)
    """
    # Clear any existing handlers to prevent duplicates
    if app.logger.hasHandlers():
        app.logger.handlers.clear()

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.NOTSET)  # Handler level unset; app.logger controls level

    app.logger.addHandler(handler)
    app.logger.setLevel(level)
    app.logger.propagate = False  # Prevent double logging if root logger also logs


