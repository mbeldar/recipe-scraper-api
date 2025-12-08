"""
Logging configuration for Recipe Scraper API
Configures logging to both console and error log files
"""

import logging
import logging.handlers
import os
from pathlib import Path


def setup_logging(app=None, log_dir='logs'):
    """
    Configure logging for the application.
    
    Sets up:
    - Console handler for INFO level and above
    - File handler for ERROR level and above (error.log)
    - File handler for all levels (app.log)
    
    Args:
        app: Flask app instance (optional)
        log_dir: Directory to store log files (default: 'logs')
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    error_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console Handler - INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(console_handler)
    
    # Error File Handler - ERROR and above
    error_file_path = log_path / 'error.log'
    error_handler = logging.handlers.RotatingFileHandler(
        error_file_path,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,  # Keep 5 backup files
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(error_formatter)
    root_logger.addHandler(error_handler)
    
    # Application File Handler - DEBUG and above
    app_file_path = log_path / 'app.log'
    app_handler = logging.handlers.RotatingFileHandler(
        app_file_path,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,  # Keep 5 backup files
        encoding='utf-8'
    )
    app_handler.setLevel(logging.DEBUG)
    app_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(app_handler)
    
    # Suppress noisy third-party loggers
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    if app:
        app.logger.handlers = []
        app.logger.addHandler(console_handler)
        app.logger.addHandler(error_handler)
        app.logger.addHandler(app_handler)
        app.logger.setLevel(logging.DEBUG)
    
    root_logger.info("Logging configured successfully. Error logs: %s", error_file_path)
