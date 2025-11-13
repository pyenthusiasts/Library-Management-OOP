"""Unit tests for the Library model."""

import pytest
from datetime import datetime, timedelta

from library_system.models import Library, Book, Member, BookCategory
from library_system.exceptions import (
    BookNotFoundError,
    MemberNotFoundError,
    DuplicateBookError,
    DuplicateMemberError,
)


class TestLibrary:
    """Test cases for the Library class."""

    def test_library_creation(self):
        """Test creating a library."""
        library = Library("City Library")

        assert library.name == "City Library"
        assert len(library.get_all_books()) == 0
        assert len(library.get_all_members()) == 0

    def test_library_add_book(self):
        """Test adding a book to the library."""
        library = Library()
        book = Book("Test Book", "Test Author", "9780743273565")

        library.add_book(book)

        assert len(library.get_all_books()) == 1
        assert library.get_book("9780743273565") == book

    def test_library_add_duplicate_book(self):
        """Test adding a duplicate book."""
        library = Library()
        book1 = Book("Book 1", "Author 1", "9780743273565")
        book2 = Book("Book 2", "Author 2", "9780743273565")

        library.add_book(book1)

        with pytest.raises(DuplicateBookError):
            library.add_book(book2)

    def test_library_remove_book(self):
        """Test removing a book from the library."""
        library = Library()
        book = Book("Test Book", "Test Author", "9780743273565")

        library.add_book(book)
        removed_book = library.remove_book("9780743273565")

        assert removed_book == book
        assert len(library.get_all_books()) == 0

    def test_library_remove_nonexistent_book(self):
        """Test removing a book that doesn't exist."""
        library = Library()

        with pytest.raises(BookNotFoundError):
            library.remove_book("9780743273565")

    def test_library_get_book(self):
        """Test getting a book by ISBN."""
        library = Library()
        book = Book("Test Book", "Test Author", "9780743273565")

        library.add_book(book)
        retrieved_book = library.get_book("9780743273565")

        assert retrieved_book == book

    def test_library_find_books_by_title(self):
        """Test finding books by title."""
        library = Library()
        book1 = Book("The Great Book", "Author 1", "9780743273565")
        book2 = Book("Great Expectations", "Author 2", "9780061120084")
        book3 = Book("Other Book", "Author 3", "9780451524935")

        library.add_book(book1)
        library.add_book(book2)
        library.add_book(book3)

        results = library.find_books_by_title("Great")
        assert len(results) == 2
        assert book1 in results
        assert book2 in results

    def test_library_find_books_by_author(self):
        """Test finding books by author."""
        library = Library()
        book1 = Book("Book 1", "John Smith", "9780743273565")
        book2 = Book("Book 2", "Jane Smith", "9780061120084")
        book3 = Book("Book 3", "Bob Jones", "9780451524935")

        library.add_book(book1)
        library.add_book(book2)
        library.add_book(book3)

        results = library.find_books_by_author("Smith")
        assert len(results) == 2
        assert book1 in results
        assert book2 in results

    def test_library_find_books_by_category(self):
        """Test finding books by category."""
        library = Library()
        book1 = Book("Book 1", "Author 1", "9780743273565", BookCategory.FICTION)
        book2 = Book("Book 2", "Author 2", "9780061120084", BookCategory.FICTION)
        book3 = Book("Book 3", "Author 3", "9780451524935", BookCategory.SCIENCE)

        library.add_book(book1)
        library.add_book(book2)
        library.add_book(book3)

        results = library.find_books_by_category(BookCategory.FICTION)
        assert len(results) == 2
        assert book1 in results
        assert book2 in results

    def test_library_get_available_books(self):
        """Test getting available books."""
        library = Library()
        book1 = Book("Book 1", "Author 1", "9780743273565")
        book2 = Book("Book 2", "Author 2", "9780061120084")
        member = Member("John Doe", "john@example.com", "M001")

        library.add_book(book1)
        library.add_book(book2)
        library.add_member(member)

        member.borrow_book(book1)

        available = library.get_available_books()
        assert len(available) == 1
        assert book2 in available

    def test_library_add_member(self):
        """Test adding a member to the library."""
        library = Library()
        member = Member("John Doe", "john@example.com", "M001")

        library.add_member(member)

        assert len(library.get_all_members()) == 1
        assert library.get_member("M001") == member

    def test_library_add_duplicate_member(self):
        """Test adding a duplicate member."""
        library = Library()
        member1 = Member("John Doe", "john@example.com", "M001")
        member2 = Member("Jane Doe", "jane@example.com", "M001")

        library.add_member(member1)

        with pytest.raises(DuplicateMemberError):
            library.add_member(member2)

    def test_library_remove_member(self):
        """Test removing a member from the library."""
        library = Library()
        member = Member("John Doe", "john@example.com", "M001")

        library.add_member(member)
        removed_member = library.remove_member("M001")

        assert removed_member == member
        assert len(library.get_all_members()) == 0

    def test_library_remove_member_with_borrowed_books(self):
        """Test removing a member who has borrowed books."""
        library = Library()
        member = Member("John Doe", "john@example.com", "M001")
        book = Book("Test Book", "Test Author", "9780743273565")

        library.add_member(member)
        library.add_book(book)
        member.borrow_book(book)

        with pytest.raises(ValueError, match="borrowed books"):
            library.remove_member("M001")

    def test_library_get_statistics(self):
        """Test getting library statistics."""
        library = Library()
        book1 = Book("Book 1", "Author 1", "9780743273565")
        book2 = Book("Book 2", "Author 2", "9780061120084")
        book3 = Book("Book 3", "Author 3", "9780451524935")
        member = Member("John Doe", "john@example.com", "M001")

        library.add_book(book1)
        library.add_book(book2)
        library.add_book(book3)
        library.add_member(member)

        member.borrow_book(book1)

        # Make book1 overdue
        book1._due_date = datetime.now() - timedelta(days=5)

        stats = library.get_statistics()

        assert stats["total_books"] == 3
        assert stats["available_books"] == 2
        assert stats["borrowed_books"] == 1
        assert stats["overdue_books"] == 1
        assert stats["total_members"] == 1
        assert stats["members_with_overdue"] == 1
