"""
Logging configuration utility for the crypto-agent project
"""
import os
import logging


def setup_logger(name: str, log_filename: str = None) -> logging.Logger:
    """
    Set up logger with both console and file output

    Args:
        name: Logger name (typically __name__)
        log_filename: Optional custom log filename (defaults to {name}.log)

    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create formatters
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    if not log_filename:
        log_filename = f"{name.split('.')[-1]}.log"

    file_handler = logging.FileHandler(os.path.join(log_dir, log_filename))
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger