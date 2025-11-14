"""Environment configuration with validation."""

import os
from typing import Optional, Any
from pathlib import Path
import logging

from ..utils.logging_config import get_logger

logger = get_logger(__name__)


class EnvConfig:
    """
    Environment-based configuration with validation and defaults.

    Loads configuration from environment variables with proper typing
    and validation.
    """

    def __init__(self, env_file: Optional[Path] = None) -> None:
        """
        Initialize environment configuration.

        Args:
            env_file: Path to .env file to load (optional).
        """
        if env_file and env_file.exists():
            self._load_env_file(env_file)

    @staticmethod
    def _load_env_file(env_file: Path) -> None:
        """Load environment variables from a .env file."""
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip()
            logger.info(f"Loaded environment from {env_file}")
        except Exception as e:
            logger.error(f"Failed to load .env file: {e}")

    @staticmethod
    def get_str(key: str, default: str = "") -> str:
        """Get string environment variable."""
        return os.getenv(key, default)

    @staticmethod
    def get_int(key: str, default: int = 0) -> int:
        """Get integer environment variable."""
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            logger.warning(f"Invalid integer value for {key}: {value}, using default: {default}")
            return default

    @staticmethod
    def get_float(key: str, default: float = 0.0) -> float:
        """Get float environment variable."""
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return float(value)
        except ValueError:
            logger.warning(f"Invalid float value for {key}: {value}, using default: {default}")
            return default

    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        """Get boolean environment variable."""
        value = os.getenv(key, "").lower()
        if not value:
            return default
        return value in ("true", "1", "yes", "on")

    @staticmethod
    def get_path(key: str, default: str = "") -> Path:
        """Get path environment variable."""
        return Path(os.getenv(key, default))

    @staticmethod
    def get_log_level(key: str = "LOG_LEVEL", default: str = "INFO") -> int:
        """Get logging level from environment."""
        level_str = os.getenv(key, default).upper()
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        return level_map.get(level_str, logging.INFO)

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate required environment variables.

        Returns:
            Tuple of (is_valid, error_messages).
        """
        errors = []

        # Validate library name
        library_name = self.get_str("LIBRARY_NAME")
        if not library_name:
            errors.append("LIBRARY_NAME is not set")

        # Validate numeric values
        max_books = self.get_int("MAX_BOOKS_PER_MEMBER", 5)
        if max_books <= 0:
            errors.append(f"MAX_BOOKS_PER_MEMBER must be positive, got: {max_books}")

        loan_days = self.get_int("LOAN_PERIOD_DAYS", 14)
        if loan_days <= 0:
            errors.append(f"LOAN_PERIOD_DAYS must be positive, got: {loan_days}")

        late_fee = self.get_float("LATE_FEE_PER_DAY", 0.50)
        if late_fee < 0:
            errors.append(f"LATE_FEE_PER_DAY cannot be negative, got: {late_fee}")

        # Validate storage path
        storage_path = self.get_path("STORAGE_PATH")
        if storage_path:
            storage_path.parent.mkdir(parents=True, exist_ok=True)

        is_valid = len(errors) == 0

        if not is_valid:
            for error in errors:
                logger.error(f"Environment validation error: {error}")

        return is_valid, errors

    def get_all_config(self) -> dict:
        """
        Get all configuration as a dictionary.

        Returns:
            Dictionary containing all configuration values.
        """
        return {
            "library_name": self.get_str("LIBRARY_NAME", "City Library"),
            "max_books_per_member": self.get_int("MAX_BOOKS_PER_MEMBER", 5),
            "loan_period_days": self.get_int("LOAN_PERIOD_DAYS", 14),
            "late_fee_per_day": self.get_float("LATE_FEE_PER_DAY", 0.50),
            "storage_path": str(self.get_path("STORAGE_PATH", "data/library_data.json")),
            "storage_type": self.get_str("STORAGE_TYPE", "json"),
            "log_level": self.get_str("LOG_LEVEL", "INFO"),
            "log_dir": str(self.get_path("LOG_DIR", "logs")),
            "enable_audit_log": self.get_bool("ENABLE_AUDIT_LOG", True),
            "env": self.get_str("ENV", "development"),
            "debug": self.get_bool("DEBUG", False),
        }


# Global instance
_env_config: Optional[EnvConfig] = None


def get_env_config(env_file: Optional[Path] = None) -> EnvConfig:
    """
    Get the global environment configuration instance.

    Args:
        env_file: Path to .env file (only used on first call).

    Returns:
        EnvConfig instance.
    """
    global _env_config
    if _env_config is None:
        _env_config = EnvConfig(env_file)
    return _env_config
