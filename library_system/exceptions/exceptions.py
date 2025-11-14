"""Custom exception classes for the library management system."""


class LibraryException(Exception):
    """Base exception class for all library-related exceptions."""
    pass


class BookNotAvailableError(LibraryException):
    """Raised when attempting to borrow a book that is not available."""

    def __init__(self, book_title: str):
        self.book_title = book_title
        super().__init__(f"Book '{book_title}' is not available for borrowing.")


class BookNotFoundError(LibraryException):
    """Raised when a requested book is not found in the library."""

    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Book with identifier '{identifier}' not found.")


class MemberNotFoundError(LibraryException):
    """Raised when a requested member is not found in the library."""

    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Member with identifier '{identifier}' not found.")


class InvalidISBNError(LibraryException):
    """Raised when an invalid ISBN is provided."""

    def __init__(self, isbn: str):
        self.isbn = isbn
        super().__init__(f"Invalid ISBN: '{isbn}'.")


class InvalidEmailError(LibraryException):
    """Raised when an invalid email address is provided."""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Invalid email address: '{email}'.")


class DuplicateBookError(LibraryException):
    """Raised when attempting to add a book that already exists."""

    def __init__(self, isbn: str):
        self.isbn = isbn
        super().__init__(f"Book with ISBN '{isbn}' already exists in the library.")


class DuplicateMemberError(LibraryException):
    """Raised when attempting to add a member that already exists."""

    def __init__(self, member_id: str):
        self.member_id = member_id
        super().__init__(f"Member with ID '{member_id}' already exists.")


class BookNotBorrowedError(LibraryException):
    """Raised when attempting to return a book that was not borrowed by the member."""

    def __init__(self, book_title: str, member_name: str):
        self.book_title = book_title
        self.member_name = member_name
        super().__init__(f"'{book_title}' was not borrowed by {member_name}.")
