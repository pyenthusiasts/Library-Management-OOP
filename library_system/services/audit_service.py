"""Audit logging service for tracking library operations."""

from datetime import datetime
from typing import Optional, Dict, Any
import json
from pathlib import Path

from ..utils.logging_config import get_audit_logger


class AuditService:
    """
    Service for logging audit trails of important library operations.

    Tracks all significant actions including:
    - Book additions and removals
    - Member registrations and removals
    - Borrowing and returning books
    - Configuration changes
    """

    def __init__(self) -> None:
        """Initialize the audit service."""
        self.logger = get_audit_logger()
        self.audit_file = Path("logs/audit_trail.jsonl")
        self.audit_file.parent.mkdir(exist_ok=True)

    def log_operation(
        self,
        operation: str,
        entity_type: str,
        entity_id: str,
        user: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        success: bool = True
    ) -> None:
        """
        Log an audit event.

        Args:
            operation: The operation performed (e.g., "ADD", "REMOVE", "BORROW").
            entity_type: The type of entity (e.g., "BOOK", "MEMBER").
            entity_id: The unique identifier of the entity.
            user: The user who performed the operation.
            details: Additional details about the operation.
            success: Whether the operation was successful.
        """
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "user": user or "system",
            "success": success,
            "details": details or {}
        }

        # Log to audit logger
        self.logger.info(
            f"{operation} {entity_type} {entity_id} by {audit_entry['user']} - "
            f"{'SUCCESS' if success else 'FAILED'}"
        )

        # Append to JSON Lines file
        try:
            with open(self.audit_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(audit_entry) + '\n')
        except IOError as e:
            self.logger.error(f"Failed to write audit entry: {e}")

    def log_book_added(self, isbn: str, title: str, author: str) -> None:
        """Log when a book is added."""
        self.log_operation(
            operation="ADD_BOOK",
            entity_type="BOOK",
            entity_id=isbn,
            details={"title": title, "author": author}
        )

    def log_book_removed(self, isbn: str, title: str) -> None:
        """Log when a book is removed."""
        self.log_operation(
            operation="REMOVE_BOOK",
            entity_type="BOOK",
            entity_id=isbn,
            details={"title": title}
        )

    def log_member_added(self, member_id: str, name: str, email: str) -> None:
        """Log when a member is added."""
        self.log_operation(
            operation="ADD_MEMBER",
            entity_type="MEMBER",
            entity_id=member_id,
            details={"name": name, "email": email}
        )

    def log_member_removed(self, member_id: str, name: str) -> None:
        """Log when a member is removed."""
        self.log_operation(
            operation="REMOVE_MEMBER",
            entity_type="MEMBER",
            entity_id=member_id,
            details={"name": name}
        )

    def log_book_borrowed(
        self,
        isbn: str,
        title: str,
        member_id: str,
        member_name: str,
        due_date: str
    ) -> None:
        """Log when a book is borrowed."""
        self.log_operation(
            operation="BORROW_BOOK",
            entity_type="BOOK",
            entity_id=isbn,
            user=member_id,
            details={
                "title": title,
                "member_name": member_name,
                "due_date": due_date
            }
        )

    def log_book_returned(
        self,
        isbn: str,
        title: str,
        member_id: str,
        member_name: str,
        was_overdue: bool = False,
        late_fee: float = 0.0
    ) -> None:
        """Log when a book is returned."""
        self.log_operation(
            operation="RETURN_BOOK",
            entity_type="BOOK",
            entity_id=isbn,
            user=member_id,
            details={
                "title": title,
                "member_name": member_name,
                "was_overdue": was_overdue,
                "late_fee": late_fee
            }
        )

    def get_audit_trail(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        operation: Optional[str] = None,
        entity_type: Optional[str] = None
    ) -> list:
        """
        Retrieve audit trail entries with optional filters.

        Args:
            start_date: Filter entries after this date.
            end_date: Filter entries before this date.
            operation: Filter by operation type.
            entity_type: Filter by entity type.

        Returns:
            List of audit entries matching the filters.
        """
        if not self.audit_file.exists():
            return []

        entries = []
        try:
            with open(self.audit_file, 'r', encoding='utf-8') as f:
                for line in f:
                    entry = json.loads(line.strip())

                    # Apply filters
                    if start_date and datetime.fromisoformat(entry['timestamp']) < start_date:
                        continue
                    if end_date and datetime.fromisoformat(entry['timestamp']) > end_date:
                        continue
                    if operation and entry['operation'] != operation:
                        continue
                    if entity_type and entry['entity_type'] != entity_type:
                        continue

                    entries.append(entry)
        except (IOError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to read audit trail: {e}")

        return entries
