"""Backup and restore service for library data."""

import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional
import tarfile

from ..utils.logging_config import get_logger

logger = get_logger(__name__)


class BackupService:
    """
    Service for creating and managing backups of library data.

    Provides functionality for:
    - Creating timestamped backups
    - Listing available backups
    - Restoring from backups
    - Automatic backup rotation
    """

    def __init__(
        self,
        backup_dir: Path = Path("backups"),
        max_backups: int = 10
    ) -> None:
        """
        Initialize the backup service.

        Args:
            backup_dir: Directory to store backups.
            max_backups: Maximum number of backups to keep.
        """
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.max_backups = max_backups
        logger.info(f"BackupService initialized with backup_dir={backup_dir}")

    def create_backup(
        self,
        data_path: Path = Path("data/library_data.json"),
        include_logs: bool = True,
        include_audit: bool = True
    ) -> Optional[Path]:
        """
        Create a backup of library data and optionally logs.

        Args:
            data_path: Path to the library data file.
            include_logs: Whether to include log files.
            include_audit: Whether to include audit logs.

        Returns:
            Path to the created backup file, or None if backup failed.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"library_backup_{timestamp}.tar.gz"
        backup_path = self.backup_dir / backup_name

        try:
            logger.info(f"Creating backup: {backup_name}")

            with tarfile.open(backup_path, "w:gz") as tar:
                # Backup library data
                if data_path.exists():
                    tar.add(data_path, arcname=data_path.name)
                    logger.debug(f"Added {data_path} to backup")

                # Backup logs if requested
                if include_logs and Path("logs").exists():
                    for log_file in Path("logs").glob("*.log"):
                        tar.add(log_file, arcname=f"logs/{log_file.name}")
                        logger.debug(f"Added {log_file} to backup")

                # Backup audit trail if requested
                if include_audit and Path("logs/audit_trail.jsonl").exists():
                    tar.add(
                        Path("logs/audit_trail.jsonl"),
                        arcname="logs/audit_trail.jsonl"
                    )
                    logger.debug("Added audit trail to backup")

                # Add backup metadata
                metadata = {
                    "timestamp": datetime.now().isoformat(),
                    "data_file": str(data_path),
                    "includes_logs": include_logs,
                    "includes_audit": include_audit
                }
                metadata_file = self.backup_dir / "metadata.json"
                metadata_file.write_text(json.dumps(metadata, indent=2))
                tar.add(metadata_file, arcname="metadata.json")

            logger.info(f"Backup created successfully: {backup_path}")

            # Rotate old backups
            self._rotate_backups()

            return backup_path

        except Exception as e:
            logger.error(f"Failed to create backup: {e}", exc_info=True)
            return None

    def restore_backup(
        self,
        backup_path: Path,
        restore_logs: bool = True,
        restore_audit: bool = True
    ) -> bool:
        """
        Restore library data from a backup.

        Args:
            backup_path: Path to the backup file.
            restore_logs: Whether to restore log files.
            restore_audit: Whether to restore audit logs.

        Returns:
            True if restoration was successful, False otherwise.
        """
        if not backup_path.exists():
            logger.error(f"Backup file not found: {backup_path}")
            return False

        try:
            logger.info(f"Restoring from backup: {backup_path}")

            # Create temporary extraction directory
            temp_dir = self.backup_dir / "temp_restore"
            temp_dir.mkdir(exist_ok=True)

            try:
                with tarfile.open(backup_path, "r:gz") as tar:
                    tar.extractall(temp_dir)

                # Restore library data
                data_file = temp_dir / "library_data.json"
                if data_file.exists():
                    shutil.copy2(data_file, Path("data/library_data.json"))
                    logger.info("Library data restored")

                # Restore logs if requested
                if restore_logs:
                    logs_dir = temp_dir / "logs"
                    if logs_dir.exists():
                        Path("logs").mkdir(exist_ok=True)
                        for log_file in logs_dir.glob("*.log"):
                            shutil.copy2(log_file, Path("logs") / log_file.name)
                        logger.info("Log files restored")

                # Restore audit trail if requested
                if restore_audit:
                    audit_file = temp_dir / "logs" / "audit_trail.jsonl"
                    if audit_file.exists():
                        Path("logs").mkdir(exist_ok=True)
                        shutil.copy2(audit_file, Path("logs/audit_trail.jsonl"))
                        logger.info("Audit trail restored")

                logger.info("Restore completed successfully")
                return True

            finally:
                # Clean up temporary directory
                shutil.rmtree(temp_dir, ignore_errors=True)

        except Exception as e:
            logger.error(f"Failed to restore backup: {e}", exc_info=True)
            return False

    def list_backups(self) -> List[dict]:
        """
        List all available backups with metadata.

        Returns:
            List of dictionaries containing backup information.
        """
        backups = []

        for backup_file in sorted(self.backup_dir.glob("library_backup_*.tar.gz")):
            # Extract timestamp from filename
            try:
                timestamp_str = backup_file.stem.replace("library_backup_", "")
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")

                backup_info = {
                    "filename": backup_file.name,
                    "path": str(backup_file),
                    "timestamp": timestamp.isoformat(),
                    "size_bytes": backup_file.stat().st_size,
                    "size_mb": round(backup_file.stat().st_size / (1024 * 1024), 2)
                }
                backups.append(backup_info)

            except ValueError:
                logger.warning(f"Skipping invalid backup filename: {backup_file}")
                continue

        return backups

    def get_latest_backup(self) -> Optional[Path]:
        """
        Get the path to the most recent backup.

        Returns:
            Path to the latest backup, or None if no backups exist.
        """
        backups = sorted(self.backup_dir.glob("library_backup_*.tar.gz"))
        return backups[-1] if backups else None

    def delete_backup(self, backup_path: Path) -> bool:
        """
        Delete a specific backup file.

        Args:
            backup_path: Path to the backup to delete.

        Returns:
            True if deletion was successful, False otherwise.
        """
        try:
            if backup_path.exists():
                backup_path.unlink()
                logger.info(f"Deleted backup: {backup_path}")
                return True
            else:
                logger.warning(f"Backup not found: {backup_path}")
                return False
        except Exception as e:
            logger.error(f"Failed to delete backup: {e}")
            return False

    def _rotate_backups(self) -> None:
        """Remove old backups exceeding the maximum number to keep."""
        backups = sorted(self.backup_dir.glob("library_backup_*.tar.gz"))

        if len(backups) > self.max_backups:
            backups_to_remove = backups[:-self.max_backups]
            for backup in backups_to_remove:
                try:
                    backup.unlink()
                    logger.info(f"Rotated old backup: {backup.name}")
                except Exception as e:
                    logger.error(f"Failed to remove old backup {backup}: {e}")

    def create_scheduled_backup(self) -> Optional[Path]:
        """
        Create a backup with automatic scheduling metadata.

        This method is intended to be called by a scheduler (cron, systemd timer, etc.)

        Returns:
            Path to the created backup, or None if backup failed.
        """
        logger.info("Creating scheduled backup")
        return self.create_backup(include_logs=True, include_audit=True)
