"""Unit tests for the Book model."""

import pytest
from datetime import datetime, timedelta

from library_system.models import Book, BookCategory, Member
from library_system.exceptions import InvalidISBNError


class TestBook:
    """Test cases for the Book class."""

    def test_book_creation(self):
        """Test creating a book with valid data."""
        book = Book("Test Book", "Test Author", "9780743273565", BookCategory.FICTION, 2020)

        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.isbn == "9780743273565"
        assert book.category == BookCategory.FICTION
        assert book.publication_year == 2020
        assert book.is_available() is True

    def test_book_invalid_isbn(self):
        """Test creating a book with invalid ISBN."""
        with pytest.raises(InvalidISBNError):
            Book("Test Book", "Test Author", "invalid-isbn")

    def test_book_is_available(self):
        """Test book availability status."""
        book = Book("Test Book", "Test Author", "9780743273565")
        member = Member("John Doe", "john@example.com", "M001")

        assert book.is_available() is True

        member.borrow_book(book)
        assert book.is_available() is False

        member.return_book(book)
        assert book.is_available() is True

    def test_book_borrow(self):
        """Test borrowing a book."""
        book = Book("Test Book", "Test Author", "9780743273565")
        member = Member("John Doe", "john@example.com", "M001")

        member.borrow_book(book)

        assert book.borrower == member
        assert book.borrowed_date is not None
        assert book.due_date is not None
        assert book.is_available() is False

    def test_book_return(self):
        """Test returning a book."""
        book = Book("Test Book", "Test Author", "9780743273565")
        member = Member("John Doe", "john@example.com", "M001")

        member.borrow_book(book)
        member.return_book(book)

        assert book.borrower is None
        assert book.borrowed_date is None
        assert book.due_date is None
        assert book.is_available() is True

    def test_book_is_overdue(self):
        """Test checking if a book is overdue."""
        book = Book("Test Book", "Test Author", "9780743273565")
        member = Member("John Doe", "john@example.com", "M001")

        # Not borrowed yet
        assert book.is_overdue() is False

        # Borrow with a past due date
        book.borrow(member, loan_period_days=0)
        book._due_date = datetime.now() - timedelta(days=5)

        assert book.is_overdue() is True
        assert book.days_overdue() == 5

    def test_book_equality(self):
        """Test book equality based on ISBN."""
        book1 = Book("Book 1", "Author 1", "9780743273565")
        book2 = Book("Book 2", "Author 2", "9780743273565")
        book3 = Book("Book 3", "Author 3", "9780061120084")

        assert book1 == book2
        assert book1 != book3

    def test_book_to_dict(self):
        """Test converting book to dictionary."""
        book = Book("Test Book", "Test Author", "9780743273565", BookCategory.FICTION, 2020)
        data = book.to_dict()

        assert data["title"] == "Test Book"
        assert data["author"] == "Test Author"
        assert data["isbn"] == "9780743273565"
        assert data["category"] == "Fiction"
        assert data["publication_year"] == 2020
        assert data["is_available"] is True
