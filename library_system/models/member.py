"""Member model for the library management system."""

from typing import List, Optional
from datetime import datetime

from .person import Person
from .book import Book
from ..exceptions import BookNotAvailableError, BookNotBorrowedError


class Member(Person):
    """
    Class representing a library member.

    A member can borrow and return books from the library.

    Attributes:
        member_id: The unique identifier for the member.
        borrowed_books: A list of books currently borrowed by the member.
        membership_date: The date when the member joined the library.
        max_books: The maximum number of books the member can borrow at once.
    """

    DEFAULT_MAX_BOOKS = 5

    def __init__(
        self,
        name: str,
        email: str,
        member_id: str,
        max_books: int = DEFAULT_MAX_BOOKS,
    ) -> None:
        """
        Initialize a Member instance.

        Args:
            name: The name of the member.
            email: The email address of the member.
            member_id: The unique identifier for the member.
            max_books: The maximum number of books the member can borrow.

        Raises:
            InvalidEmailError: If the email address is invalid.
        """
        super().__init__(name, email)
        self._member_id = member_id
        self._borrowed_books: List[Book] = []
        self._membership_date = datetime.now()
        self._max_books = max_books

    @property
    def member_id(self) -> str:
        """Get the member's ID."""
        return self._member_id

    @property
    def membership_date(self) -> datetime:
        """Get the date when the member joined."""
        return self._membership_date

    @property
    def max_books(self) -> int:
        """Get the maximum number of books the member can borrow."""
        return self._max_books

    @max_books.setter
    def max_books(self, value: int) -> None:
        """Set the maximum number of books the member can borrow."""
        if value < 0:
            raise ValueError("Maximum books must be a positive number.")
        self._max_books = value

    def can_borrow(self) -> bool:
        """
        Check if the member can borrow more books.

        Returns:
            True if the member can borrow more books, False otherwise.
        """
        return len(self._borrowed_books) < self._max_books

    def borrow_book(self, book: Book) -> None:
        """
        Borrow a book from the library.

        Args:
            book: The book to borrow.

        Raises:
            BookNotAvailableError: If the book is not available.
            ValueError: If the member has reached their borrowing limit.
        """
        if not book.is_available():
            raise BookNotAvailableError(book.title)

        if not self.can_borrow():
            raise ValueError(
                f"Cannot borrow more books. Maximum limit of {self._max_books} reached."
            )

        self._borrowed_books.append(book)
        book.borrow(self)

    def return_book(self, book: Book) -> None:
        """
        Return a borrowed book to the library.

        Args:
            book: The book to return.

        Raises:
            BookNotBorrowedError: If the book was not borrowed by this member.
        """
        if book not in self._borrowed_books:
            raise BookNotBorrowedError(book.title, self.name)

        self._borrowed_books.remove(book)
        book.return_book()

    def get_borrowed_books(self) -> List[Book]:
        """
        Get the list of books currently borrowed by the member.

        Returns:
            A list of Book objects.
        """
        return self._borrowed_books.copy()

    def get_borrowed_book_titles(self) -> List[str]:
        """
        Get the titles of books currently borrowed by the member.

        Returns:
            A list of book titles.
        """
        return [book.title for book in self._borrowed_books]

    def has_overdue_books(self) -> bool:
        """
        Check if the member has any overdue books.

        Returns:
            True if the member has overdue books, False otherwise.
        """
        return any(book.is_overdue() for book in self._borrowed_books)

    def get_overdue_books(self) -> List[Book]:
        """
        Get the list of overdue books.

        Returns:
            A list of overdue Book objects.
        """
        return [book for book in self._borrowed_books if book.is_overdue()]

    def calculate_late_fees(self, fee_per_day: float = 0.50) -> float:
        """
        Calculate total late fees for overdue books.

        Args:
            fee_per_day: The fee charged per day for overdue books.

        Returns:
            The total late fees owed.
        """
        total_fee = 0.0
        for book in self._borrowed_books:
            if book.is_overdue():
                total_fee += book.days_overdue() * fee_per_day
        return total_fee

    def get_details(self) -> str:
        """
        Get the details of the member.

        Returns:
            A string representation of the member's details.
        """
        borrowed_count = len(self._borrowed_books)
        overdue_count = len(self.get_overdue_books())
        return (
            f"Member ID: {self._member_id}, Name: {self.name}, Email: {self.email}, "
            f"Books Borrowed: {borrowed_count}/{self._max_books}, Overdue: {overdue_count}"
        )

    def to_dict(self) -> dict:
        """
        Convert the member to a dictionary.

        Returns:
            A dictionary representation of the member.
        """
        return {
            "member_id": self._member_id,
            "name": self.name,
            "email": self.email,
            "membership_date": self._membership_date.isoformat(),
            "max_books": self._max_books,
            "borrowed_books": [book.isbn for book in self._borrowed_books],
        }

    def __str__(self) -> str:
        """Return a string representation of the member."""
        return f"Member: {self.name} (ID: {self._member_id})"

    def __repr__(self) -> str:
        """Return a detailed string representation of the member."""
        return f"Member(name='{self.name}', email='{self.email}', member_id='{self._member_id}')"
