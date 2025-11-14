"""Settings and configuration for the library management system."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import json


@dataclass
class Settings:
    """
    Configuration settings for the library management system.

    Attributes:
        library_name: The name of the library.
        max_books_per_member: Default maximum books a member can borrow.
        loan_period_days: Default loan period in days.
        late_fee_per_day: Late fee charged per day for overdue books.
        storage_path: Path to the storage file.
    """

    library_name: str = "City Library"
    max_books_per_member: int = 5
    loan_period_days: int = 14
    late_fee_per_day: float = 0.50
    storage_path: str = "data/library_data.json"

    @classmethod
    def load_from_file(cls, config_path: Path) -> "Settings":
        """
        Load settings from a JSON configuration file.

        Args:
            config_path: Path to the configuration file.

        Returns:
            A Settings instance with the loaded configuration.

        Raises:
            FileNotFoundError: If the config file doesn't exist.
            ValueError: If the config file contains invalid JSON.
        """
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")

        return cls(**data)

    def save_to_file(self, config_path: Path) -> None:
        """
        Save settings to a JSON configuration file.

        Args:
            config_path: Path to the configuration file.

        Raises:
            IOError: If there's an error writing to the file.
        """
        config_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "library_name": self.library_name,
            "max_books_per_member": self.max_books_per_member,
            "loan_period_days": self.loan_period_days,
            "late_fee_per_day": self.late_fee_per_day,
            "storage_path": self.storage_path,
        }

        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            raise IOError(f"Failed to save configuration: {e}")

    @classmethod
    def load_or_default(cls, config_path: Optional[Path] = None) -> "Settings":
        """
        Load settings from a file or return default settings if file doesn't exist.

        Args:
            config_path: Path to the configuration file.

        Returns:
            A Settings instance.
        """
        if config_path is None:
            config_path = Path("config/library_config.json")

        if config_path.exists():
            try:
                return cls.load_from_file(config_path)
            except (FileNotFoundError, ValueError):
                return cls()
        else:
            return cls()
