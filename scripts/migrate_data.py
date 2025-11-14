#!/usr/bin/env python3
"""
Data migration script for the library management system.

This script helps migrate data between different versions or formats.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import argparse

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from library_system.services import StorageService, BackupService
from library_system.utils.logging_config import get_logger

logger = get_logger(__name__)


def migrate_v1_to_v2(input_file: Path, output_file: Path) -> bool:
    """
    Migrate from v1.0 format to v2.0 format.

    Args:
        input_file: Path to v1.0 data file.
        output_file: Path for v2.0 data file.

    Returns:
        True if migration was successful.
    """
    try:
        logger.info(f"Migrating from {input_file} to {output_file}")

        # This is a placeholder for actual migration logic
        # In a real scenario, you would transform the data structure

        with open(input_file, 'r', encoding='utf-8') as f:
            old_data = json.load(f)

        # Transform data (example)
        new_data = {
            "name": old_data.get("name", "Library"),
            "created_date": datetime.now().isoformat(),
            "books": old_data.get("books", []),
            "members": old_data.get("members", [])
        }

        # Add version information
        new_data["version"] = "2.0.0"
        new_data["migrated_at"] = datetime.now().isoformat()

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2)

        logger.info("Migration completed successfully")
        return True

    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)
        return False


def backup_before_migration(data_file: Path) -> bool:
    """
    Create a backup before migration.

    Args:
        data_file: Path to the data file to backup.

    Returns:
        True if backup was successful.
    """
    backup_service = BackupService()
    backup_path = backup_service.create_backup(data_path=data_file)

    if backup_path:
        logger.info(f"Backup created: {backup_path}")
        return True
    else:
        logger.error("Backup failed")
        return False


def main():
    """Main migration script."""
    parser = argparse.ArgumentParser(
        description="Migrate library data between versions"
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Input data file path",
        default=Path("data/library_data.json")
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output data file path",
        default=None
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip backup before migration"
    )
    parser.add_argument(
        "--from-version",
        type=str,
        help="Source version",
        default="1.0"
    )
    parser.add_argument(
        "--to-version",
        type=str,
        help="Target version",
        default="2.0"
    )

    args = parser.parse_args()

    # Set output path
    if args.output is None:
        args.output = args.input.parent / f"{args.input.stem}_v{args.to_version}.json"

    print(f"Library Data Migration Tool")
    print(f"===========================")
    print(f"Input:  {args.input}")
    print(f"Output: {args.output}")
    print(f"Version: {args.from_version} -> {args.to_version}")
    print()

    # Check if input exists
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1

    # Create backup
    if not args.no_backup:
        print("Creating backup...")
        if not backup_before_migration(args.input):
            print("Error: Backup failed. Aborting migration.")
            print("Use --no-backup to skip backup (not recommended)")
            return 1
        print("Backup created successfully.")
        print()

    # Perform migration
    print("Starting migration...")
    if migrate_v1_to_v2(args.input, args.output):
        print(f"Migration completed successfully!")
        print(f"New data file: {args.output}")
        return 0
    else:
        print("Migration failed. Check logs for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
