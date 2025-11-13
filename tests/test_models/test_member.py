"""Unit tests for the Member model."""

import pytest
from datetime import datetime, timedelta

from library_system.models import Member, Book, BookCategory
from library_system.exceptions import (
    InvalidEmailError,
    BookNotAvailableError,
    BookNotBorrowedError,
)


class TestMember:
    """Test cases for the Member class."""

    def test_member_creation(self):
        """Test creating a member with valid data."""
        member = Member("John Doe", "john@example.com", "M001")

        assert member.name == "John Doe"
        assert member.email == "john@example.com"
        assert member.member_id == "M001"
        assert member.max_books == 5
        assert len(member.get_borrowed_books()) == 0

    def test_member_invalid_email(self):
        """Test creating a member with invalid email."""
        with pytest.raises(InvalidEmailError):
            Member("John Doe", "invalid-email", "M001")

    def test_member_borrow_book(self):
        """Test member borrowing a book."""
        member = Member("John Doe", "john@example.com", "M001")
        book = Book("Test Book", "Test Author", "9780743273565")

        member.borrow_book(book)

        assert len(member.get_borrowed_books()) == 1
        assert book in member.get_borrowed_books()
        assert book.borrower == member

    def test_member_borrow_unavailable_book(self):
        """Test borrowing a book that's not available."""
        member1 = Member("John Doe", "john@example.com", "M001")
        member2 = Member("Jane Doe", "jane@example.com", "M002")
        book = Book("Test Book", "Test Author", "9780743273565")

        member1.borrow_book(book)

        with pytest.raises(BookNotAvailableError):
            member2.borrow_book(book)

    def test_member_borrow_limit(self):
        """Test member borrowing limit."""
        member = Member("John Doe", "john@example.com", "M001", max_books=2)

        book1 = Book("Book 1", "Author 1", "9780743273565")
        book2 = Book("Book 2", "Author 2", "9780061120084")
        book3 = Book("Book 3", "Author 3", "9780451524935")

        member.borrow_book(book1)
        member.borrow_book(book2)

        with pytest.raises(ValueError, match="Maximum limit"):
            member.borrow_book(book3)

    def test_member_return_book(self):
        """Test member returning a book."""
        member = Member("John Doe", "john@example.com", "M001")
        book = Book("Test Book", "Test Author", "9780743273565")

        member.borrow_book(book)
        member.return_book(book)

        assert len(member.get_borrowed_books()) == 0
        assert book.is_available() is True

    def test_member_return_not_borrowed_book(self):
        """Test returning a book that wasn't borrowed."""
        member = Member("John Doe", "john@example.com", "M001")
        book = Book("Test Book", "Test Author", "9780743273565")

        with pytest.raises(BookNotBorrowedError):
            member.return_book(book)

    def test_member_has_overdue_books(self):
        """Test checking if member has overdue books."""
        member = Member("John Doe", "john@example.com", "M001")
        book = Book("Test Book", "Test Author", "9780743273565")

        member.borrow_book(book)
        assert member.has_overdue_books() is False

        # Make the book overdue
        book._due_date = datetime.now() - timedelta(days=5)
        assert member.has_overdue_books() is True

    def test_member_calculate_late_fees(self):
        """Test calculating late fees."""
        member = Member("John Doe", "john@example.com", "M001")
        book1 = Book("Book 1", "Author 1", "9780743273565")
        book2 = Book("Book 2", "Author 2", "9780061120084")

        member.borrow_book(book1)
        member.borrow_book(book2)

        # Make book1 5 days overdue
        book1._due_date = datetime.now() - timedelta(days=5)

        # Make book2 3 days overdue
        book2._due_date = datetime.now() - timedelta(days=3)

        fees = member.calculate_late_fees(fee_per_day=0.50)
        assert fees == 4.0  # (5 + 3) * 0.50

    def test_member_can_borrow(self):
        """Test checking if member can borrow more books."""
        member = Member("John Doe", "john@example.com", "M001", max_books=2)

        assert member.can_borrow() is True

        book1 = Book("Book 1", "Author 1", "9780743273565")
        member.borrow_book(book1)
        assert member.can_borrow() is True

        book2 = Book("Book 2", "Author 2", "9780061120084")
        member.borrow_book(book2)
        assert member.can_borrow() is False

    def test_member_to_dict(self):
        """Test converting member to dictionary."""
        member = Member("John Doe", "john@example.com", "M001")
        data = member.to_dict()

        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert data["member_id"] == "M001"
        assert data["max_books"] == 5
        assert data["borrowed_books"] == []
