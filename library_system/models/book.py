"""Book model for the library management system."""

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, TYPE_CHECKING

from ..exceptions import InvalidISBNError
from ..utils import validate_isbn

if TYPE_CHECKING:
    from .member import Member


class BookCategory(Enum):
    """Enumeration of book categories."""
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    SCIENCE = "Science"
    TECHNOLOGY = "Technology"
    HISTORY = "History"
    BIOGRAPHY = "Biography"
    MYSTERY = "Mystery"
    FANTASY = "Fantasy"
    ROMANCE = "Romance"
    THRILLER = "Thriller"
    SELF_HELP = "Self-Help"
    CHILDREN = "Children"
    OTHER = "Other"


class Book:
    """
    Class representing a book in the library.

    Attributes:
        title: The title of the book.
        author: The author of the book.
        isbn: The ISBN number of the book.
        category: The category of the book.
        publication_year: The year the book was published.
        borrower: The member who has borrowed the book, if any.
        borrowed_date: The date when the book was borrowed.
        due_date: The date when the book is due to be returned.
    """

    LOAN_PERIOD_DAYS = 14  # Default loan period

    def __init__(
        self,
        title: str,
        author: str,
        isbn: str,
        category: BookCategory = BookCategory.OTHER,
        publication_year: Optional[int] = None,
    ) -> None:
        """
        Initialize a Book instance.

        Args:
            title: The title of the book.
            author: The author of the book.
            isbn: The ISBN number of the book.
            category: The category of the book.
            publication_year: The year the book was published.

        Raises:
            InvalidISBNError: If the ISBN is invalid.
        """
        if not validate_isbn(isbn):
            raise InvalidISBNError(isbn)

        self._title = title
        self._author = author
        self._isbn = isbn
        self._category = category
        self._publication_year = publication_year
        self._borrower: Optional["Member"] = None
        self._borrowed_date: Optional[datetime] = None
        self._due_date: Optional[datetime] = None

    @property
    def title(self) -> str:
        """Get the book's title."""
        return self._title

    @property
    def author(self) -> str:
        """Get the book's author."""
        return self._author

    @property
    def isbn(self) -> str:
        """Get the book's ISBN."""
        return self._isbn

    @property
    def category(self) -> BookCategory:
        """Get the book's category."""
        return self._category

    @category.setter
    def category(self, value: BookCategory) -> None:
        """Set the book's category."""
        self._category = value

    @property
    def publication_year(self) -> Optional[int]:
        """Get the book's publication year."""
        return self._publication_year

    @property
    def borrower(self) -> Optional["Member"]:
        """Get the member who borrowed the book."""
        return self._borrower

    @property
    def borrowed_date(self) -> Optional[datetime]:
        """Get the date when the book was borrowed."""
        return self._borrowed_date

    @property
    def due_date(self) -> Optional[datetime]:
        """Get the date when the book is due."""
        return self._due_date

    def is_available(self) -> bool:
        """
        Check if the book is available for borrowing.

        Returns:
            True if the book is available, False otherwise.
        """
        return self._borrower is None

    def is_overdue(self) -> bool:
        """
        Check if the book is overdue.

        Returns:
            True if the book is overdue, False otherwise.
        """
        if self._due_date is None:
            return False
        return datetime.now() > self._due_date

    def days_overdue(self) -> int:
        """
        Get the number of days the book is overdue.

        Returns:
            The number of days overdue, or 0 if not overdue.
        """
        if not self.is_overdue():
            return 0
        return (datetime.now() - self._due_date).days

    def borrow(self, member: "Member", loan_period_days: int = LOAN_PERIOD_DAYS) -> None:
        """
        Mark the book as borrowed by a member.

        Args:
            member: The member borrowing the book.
            loan_period_days: The number of days for the loan period.
        """
        self._borrower = member
        self._borrowed_date = datetime.now()
        self._due_date = self._borrowed_date + timedelta(days=loan_period_days)

    def return_book(self) -> None:
        """Mark the book as returned."""
        self._borrower = None
        self._borrowed_date = None
        self._due_date = None

    def to_dict(self) -> dict:
        """
        Convert the book to a dictionary.

        Returns:
            A dictionary representation of the book.
        """
        return {
            "title": self._title,
            "author": self._author,
            "isbn": self._isbn,
            "category": self._category.value,
            "publication_year": self._publication_year,
            "is_available": self.is_available(),
            "borrower_id": self._borrower.member_id if self._borrower else None,
            "borrowed_date": self._borrowed_date.isoformat() if self._borrowed_date else None,
            "due_date": self._due_date.isoformat() if self._due_date else None,
        }

    def __str__(self) -> str:
        """Return a string representation of the book."""
        status = "Available" if self.is_available() else f"Borrowed by {self._borrower.name}"
        year = f", {self._publication_year}" if self._publication_year else ""
        return f"'{self._title}' by {self._author} [{self._category.value}]{year} - ISBN: {self._isbn} ({status})"

    def __repr__(self) -> str:
        """Return a detailed string representation of the book."""
        return f"Book(title='{self._title}', author='{self._author}', isbn='{self._isbn}')"

    def __eq__(self, other: object) -> bool:
        """Check equality based on ISBN."""
        if not isinstance(other, Book):
            return NotImplemented
        return self._isbn == other._isbn

    def __hash__(self) -> int:
        """Hash based on ISBN."""
        return hash(self._isbn)
