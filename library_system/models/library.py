"""Library model for managing books and members."""

from typing import List, Optional, Dict
from datetime import datetime

from .book import Book, BookCategory
from .member import Member
from ..exceptions import (
    BookNotFoundError,
    MemberNotFoundError,
    DuplicateBookError,
    DuplicateMemberError,
)


class Library:
    """
    Class representing the library.

    Manages the collection of books and members, providing functionality
    for adding, removing, searching, and managing library operations.

    Attributes:
        name: The name of the library.
        books: A dictionary of books indexed by ISBN.
        members: A dictionary of members indexed by member ID.
    """

    def __init__(self, name: str = "Library") -> None:
        """
        Initialize a Library instance.

        Args:
            name: The name of the library.
        """
        self._name = name
        self._books: Dict[str, Book] = {}
        self._members: Dict[str, Member] = {}
        self._created_date = datetime.now()

    @property
    def name(self) -> str:
        """Get the library's name."""
        return self._name

    @property
    def created_date(self) -> datetime:
        """Get the date when the library was created."""
        return self._created_date

    # Book management methods

    def add_book(self, book: Book) -> None:
        """
        Add a book to the library.

        Args:
            book: The book to add.

        Raises:
            DuplicateBookError: If a book with the same ISBN already exists.
        """
        if book.isbn in self._books:
            raise DuplicateBookError(book.isbn)

        self._books[book.isbn] = book

    def remove_book(self, isbn: str) -> Book:
        """
        Remove a book from the library by ISBN.

        Args:
            isbn: The ISBN of the book to remove.

        Returns:
            The removed book.

        Raises:
            BookNotFoundError: If the book is not found.
        """
        if isbn not in self._books:
            raise BookNotFoundError(isbn)

        return self._books.pop(isbn)

    def get_book(self, isbn: str) -> Book:
        """
        Get a book by ISBN.

        Args:
            isbn: The ISBN of the book.

        Returns:
            The requested book.

        Raises:
            BookNotFoundError: If the book is not found.
        """
        if isbn not in self._books:
            raise BookNotFoundError(isbn)

        return self._books[isbn]

    def find_books_by_title(self, title: str, exact: bool = False) -> List[Book]:
        """
        Find books by title.

        Args:
            title: The title to search for.
            exact: If True, search for exact matches only.

        Returns:
            A list of matching books.
        """
        if exact:
            return [book for book in self._books.values() if book.title == title]
        else:
            title_lower = title.lower()
            return [
                book for book in self._books.values()
                if title_lower in book.title.lower()
            ]

    def find_books_by_author(self, author: str, exact: bool = False) -> List[Book]:
        """
        Find books by author.

        Args:
            author: The author to search for.
            exact: If True, search for exact matches only.

        Returns:
            A list of matching books.
        """
        if exact:
            return [book for book in self._books.values() if book.author == author]
        else:
            author_lower = author.lower()
            return [
                book for book in self._books.values()
                if author_lower in book.author.lower()
            ]

    def find_books_by_category(self, category: BookCategory) -> List[Book]:
        """
        Find books by category.

        Args:
            category: The category to search for.

        Returns:
            A list of matching books.
        """
        return [book for book in self._books.values() if book.category == category]

    def get_all_books(self) -> List[Book]:
        """
        Get all books in the library.

        Returns:
            A list of all books.
        """
        return list(self._books.values())

    def get_available_books(self) -> List[Book]:
        """
        Get all available books.

        Returns:
            A list of available books.
        """
        return [book for book in self._books.values() if book.is_available()]

    def get_borrowed_books(self) -> List[Book]:
        """
        Get all borrowed books.

        Returns:
            A list of borrowed books.
        """
        return [book for book in self._books.values() if not book.is_available()]

    def get_overdue_books(self) -> List[Book]:
        """
        Get all overdue books.

        Returns:
            A list of overdue books.
        """
        return [book for book in self._books.values() if book.is_overdue()]

    # Member management methods

    def add_member(self, member: Member) -> None:
        """
        Add a member to the library.

        Args:
            member: The member to add.

        Raises:
            DuplicateMemberError: If a member with the same ID already exists.
        """
        if member.member_id in self._members:
            raise DuplicateMemberError(member.member_id)

        self._members[member.member_id] = member

    def remove_member(self, member_id: str) -> Member:
        """
        Remove a member from the library.

        Args:
            member_id: The ID of the member to remove.

        Returns:
            The removed member.

        Raises:
            MemberNotFoundError: If the member is not found.
            ValueError: If the member has borrowed books.
        """
        if member_id not in self._members:
            raise MemberNotFoundError(member_id)

        member = self._members[member_id]
        if member.get_borrowed_books():
            raise ValueError(
                f"Cannot remove member {member.name}. They have borrowed books."
            )

        return self._members.pop(member_id)

    def get_member(self, member_id: str) -> Member:
        """
        Get a member by ID.

        Args:
            member_id: The ID of the member.

        Returns:
            The requested member.

        Raises:
            MemberNotFoundError: If the member is not found.
        """
        if member_id not in self._members:
            raise MemberNotFoundError(member_id)

        return self._members[member_id]

    def find_members_by_name(self, name: str, exact: bool = False) -> List[Member]:
        """
        Find members by name.

        Args:
            name: The name to search for.
            exact: If True, search for exact matches only.

        Returns:
            A list of matching members.
        """
        if exact:
            return [member for member in self._members.values() if member.name == name]
        else:
            name_lower = name.lower()
            return [
                member for member in self._members.values()
                if name_lower in member.name.lower()
            ]

    def get_all_members(self) -> List[Member]:
        """
        Get all members in the library.

        Returns:
            A list of all members.
        """
        return list(self._members.values())

    def get_members_with_overdue_books(self) -> List[Member]:
        """
        Get all members with overdue books.

        Returns:
            A list of members with overdue books.
        """
        return [member for member in self._members.values() if member.has_overdue_books()]

    # Statistics methods

    def get_statistics(self) -> Dict[str, int]:
        """
        Get library statistics.

        Returns:
            A dictionary containing library statistics.
        """
        return {
            "total_books": len(self._books),
            "available_books": len(self.get_available_books()),
            "borrowed_books": len(self.get_borrowed_books()),
            "overdue_books": len(self.get_overdue_books()),
            "total_members": len(self._members),
            "members_with_overdue": len(self.get_members_with_overdue_books()),
        }

    def to_dict(self) -> dict:
        """
        Convert the library to a dictionary.

        Returns:
            A dictionary representation of the library.
        """
        return {
            "name": self._name,
            "created_date": self._created_date.isoformat(),
            "books": [book.to_dict() for book in self._books.values()],
            "members": [member.to_dict() for member in self._members.values()],
        }

    def __str__(self) -> str:
        """Return a string representation of the library."""
        stats = self.get_statistics()
        return (
            f"{self._name}\n"
            f"Total Books: {stats['total_books']} "
            f"(Available: {stats['available_books']}, Borrowed: {stats['borrowed_books']})\n"
            f"Total Members: {stats['total_members']}"
        )

    def __repr__(self) -> str:
        """Return a detailed string representation of the library."""
        return f"Library(name='{self._name}', books={len(self._books)}, members={len(self._members)})"
