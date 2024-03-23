import logging
import os
from config import LOG_LEVEL, LOG_FORMAT

def setup_logger(name):
    """Set up a logger with the specified name and configuration from config.py"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))

    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f'logs/{name}.log')

    # Set format
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger