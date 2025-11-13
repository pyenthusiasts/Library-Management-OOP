"""Logging configuration for the library management system."""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional
import sys


class LibraryLogger:
    """
    Centralized logging configuration for the library management system.

    Provides structured logging with file rotation, console output,
    and different log levels for different components.
    """

    _instance: Optional['LibraryLogger'] = None
    _initialized: bool = False

    def __new__(cls) -> 'LibraryLogger':
        """Singleton pattern to ensure only one logger instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the logger if not already initialized."""
        if not LibraryLogger._initialized:
            self._setup_logging()
            LibraryLogger._initialized = True

    def _setup_logging(self) -> None:
        """Configure logging handlers and formatters."""
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        simple_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )

        # Root logger configuration
        self.root_logger = logging.getLogger('library_system')
        self.root_logger.setLevel(logging.DEBUG)

        # Remove existing handlers
        self.root_logger.handlers.clear()

        # Console handler (INFO and above)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        self.root_logger.addHandler(console_handler)

        # File handler with rotation (DEBUG and above)
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "library_system.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        self.root_logger.addHandler(file_handler)

        # Error file handler (ERROR and above)
        error_handler = logging.handlers.RotatingFileHandler(
            log_dir / "library_errors.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        self.root_logger.addHandler(error_handler)

        # Audit log handler (separate file for audit trail)
        audit_handler = logging.handlers.RotatingFileHandler(
            log_dir / "library_audit.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        audit_handler.setLevel(logging.INFO)
        audit_handler.setFormatter(detailed_formatter)

        # Create audit logger
        self.audit_logger = logging.getLogger('library_system.audit')
        self.audit_logger.setLevel(logging.INFO)
        self.audit_logger.addHandler(audit_handler)
        self.audit_logger.propagate = False

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a logger instance for a specific module.

        Args:
            name: The name of the logger (typically __name__).

        Returns:
            A configured logger instance.
        """
        # Ensure logging is initialized
        LibraryLogger()
        return logging.getLogger(f'library_system.{name}')

    @staticmethod
    def get_audit_logger() -> logging.Logger:
        """
        Get the audit logger for tracking important operations.

        Returns:
            The audit logger instance.
        """
        # Ensure logging is initialized
        LibraryLogger()
        return logging.getLogger('library_system.audit')

    @staticmethod
    def set_level(level: int) -> None:
        """
        Set the logging level for all handlers.

        Args:
            level: The logging level (e.g., logging.DEBUG, logging.INFO).
        """
        logger = logging.getLogger('library_system')
        logger.setLevel(level)
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """
    Convenience function to get a logger.

    Args:
        name: The name of the logger (typically __name__).

    Returns:
        A configured logger instance.
    """
    return LibraryLogger.get_logger(name)


def get_audit_logger() -> logging.Logger:
    """
    Convenience function to get the audit logger.

    Returns:
        The audit logger instance.
    """
    return LibraryLogger.get_audit_logger()
