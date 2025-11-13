# API Documentation

## Table of Contents

1. [Models](#models)
   - [Book](#book)
   - [Member](#member)
   - [Library](#library)
2. [Services](#services)
   - [StorageService](#storageservice)
3. [Configuration](#configuration)
   - [Settings](#settings)
4. [Exceptions](#exceptions)

---

## Models

### Book

Represents a book in the library system.

#### Constructor

```python
Book(title: str, author: str, isbn: str, category: BookCategory = BookCategory.OTHER, publication_year: Optional[int] = None)
```

**Parameters:**
- `title`: The title of the book
- `author`: The author of the book
- `isbn`: The ISBN number (validated)
- `category`: The book category (default: OTHER)
- `publication_year`: The publication year (optional)

**Raises:**
- `InvalidISBNError`: If the ISBN is invalid

#### Properties

- `title` (str): The book's title
- `author` (str): The book's author
- `isbn` (str): The book's ISBN
- `category` (BookCategory): The book's category
- `publication_year` (Optional[int]): Publication year
- `borrower` (Optional[Member]): Current borrower
- `borrowed_date` (Optional[datetime]): When the book was borrowed
- `due_date` (Optional[datetime]): When the book is due

#### Methods

##### `is_available() -> bool`
Check if the book is available for borrowing.

##### `is_overdue() -> bool`
Check if the book is overdue.

##### `days_overdue() -> int`
Get the number of days the book is overdue.

##### `borrow(member: Member, loan_period_days: int = 14) -> None`
Mark the book as borrowed by a member.

##### `return_book() -> None`
Mark the book as returned.

##### `to_dict() -> dict`
Convert the book to a dictionary representation.

---

### Member

Represents a library member.

#### Constructor

```python
Member(name: str, email: str, member_id: str, max_books: int = 5)
```

**Parameters:**
- `name`: The member's name
- `email`: The member's email address (validated)
- `member_id`: Unique member identifier
- `max_books`: Maximum books the member can borrow (default: 5)

**Raises:**
- `InvalidEmailError`: If the email is invalid

#### Properties

- `name` (str): The member's name
- `email` (str): The member's email
- `member_id` (str): Unique identifier
- `membership_date` (datetime): When the member joined
- `max_books` (int): Maximum borrowing limit

#### Methods

##### `can_borrow() -> bool`
Check if the member can borrow more books.

##### `borrow_book(book: Book) -> None`
Borrow a book from the library.

**Raises:**
- `BookNotAvailableError`: If the book is not available
- `ValueError`: If the member has reached their borrowing limit

##### `return_book(book: Book) -> None`
Return a borrowed book.

**Raises:**
- `BookNotBorrowedError`: If the book was not borrowed by this member

##### `get_borrowed_books() -> List[Book]`
Get the list of books currently borrowed.

##### `has_overdue_books() -> bool`
Check if the member has any overdue books.

##### `get_overdue_books() -> List[Book]`
Get the list of overdue books.

##### `calculate_late_fees(fee_per_day: float = 0.50) -> float`
Calculate total late fees for overdue books.

##### `get_details() -> str`
Get a string representation of the member's details.

##### `to_dict() -> dict`
Convert the member to a dictionary representation.

---

### Library

Represents the library system.

#### Constructor

```python
Library(name: str = "Library")
```

**Parameters:**
- `name`: The name of the library

#### Properties

- `name` (str): The library's name
- `created_date` (datetime): When the library was created

#### Book Management Methods

##### `add_book(book: Book) -> None`
Add a book to the library.

**Raises:**
- `DuplicateBookError`: If a book with the same ISBN already exists

##### `remove_book(isbn: str) -> Book`
Remove a book from the library.

**Raises:**
- `BookNotFoundError`: If the book is not found

##### `get_book(isbn: str) -> Book`
Get a book by ISBN.

**Raises:**
- `BookNotFoundError`: If the book is not found

##### `find_books_by_title(title: str, exact: bool = False) -> List[Book]`
Find books by title.

##### `find_books_by_author(author: str, exact: bool = False) -> List[Book]`
Find books by author.

##### `find_books_by_category(category: BookCategory) -> List[Book]`
Find books by category.

##### `get_all_books() -> List[Book]`
Get all books in the library.

##### `get_available_books() -> List[Book]`
Get all available books.

##### `get_borrowed_books() -> List[Book]`
Get all borrowed books.

##### `get_overdue_books() -> List[Book]`
Get all overdue books.

#### Member Management Methods

##### `add_member(member: Member) -> None`
Add a member to the library.

**Raises:**
- `DuplicateMemberError`: If a member with the same ID already exists

##### `remove_member(member_id: str) -> Member`
Remove a member from the library.

**Raises:**
- `MemberNotFoundError`: If the member is not found
- `ValueError`: If the member has borrowed books

##### `get_member(member_id: str) -> Member`
Get a member by ID.

**Raises:**
- `MemberNotFoundError`: If the member is not found

##### `find_members_by_name(name: str, exact: bool = False) -> List[Member]`
Find members by name.

##### `get_all_members() -> List[Member]`
Get all members in the library.

##### `get_members_with_overdue_books() -> List[Member]`
Get all members with overdue books.

#### Statistics Methods

##### `get_statistics() -> Dict[str, int]`
Get library statistics.

Returns a dictionary containing:
- `total_books`: Total number of books
- `available_books`: Number of available books
- `borrowed_books`: Number of borrowed books
- `overdue_books`: Number of overdue books
- `total_members`: Total number of members
- `members_with_overdue`: Number of members with overdue books

##### `to_dict() -> dict`
Convert the library to a dictionary representation.

---

## Services

### StorageService

Service for persisting library data to JSON files.

#### Constructor

```python
StorageService(storage_path: Optional[Path] = None)
```

**Parameters:**
- `storage_path`: Path to storage file (default: ./data/library_data.json)

#### Methods

##### `save_library(library: Library) -> None`
Save the library data to a JSON file.

**Raises:**
- `IOError`: If there's an error writing to the file

##### `load_library() -> Optional[Library]`
Load library data from a JSON file.

**Returns:**
- Library instance or None if file doesn't exist

**Raises:**
- `IOError`: If there's an error reading from the file
- `ValueError`: If the data is invalid

##### `delete_storage() -> None`
Delete the storage file.

##### `storage_exists() -> bool`
Check if the storage file exists.

---

## Configuration

### Settings

Configuration settings for the library system.

#### Constructor

```python
Settings(
    library_name: str = "City Library",
    max_books_per_member: int = 5,
    loan_period_days: int = 14,
    late_fee_per_day: float = 0.50,
    storage_path: str = "data/library_data.json"
)
```

#### Class Methods

##### `load_from_file(config_path: Path) -> Settings`
Load settings from a JSON configuration file.

##### `load_or_default(config_path: Optional[Path] = None) -> Settings`
Load settings from a file or return default settings.

#### Instance Methods

##### `save_to_file(config_path: Path) -> None`
Save settings to a JSON configuration file.

---

## Exceptions

### LibraryException
Base exception class for all library-related exceptions.

### BookNotAvailableError
Raised when attempting to borrow a book that is not available.

### BookNotFoundError
Raised when a requested book is not found in the library.

### MemberNotFoundError
Raised when a requested member is not found in the library.

### InvalidISBNError
Raised when an invalid ISBN is provided.

### InvalidEmailError
Raised when an invalid email address is provided.

### DuplicateBookError
Raised when attempting to add a book that already exists.

### DuplicateMemberError
Raised when attempting to add a member that already exists.

### BookNotBorrowedError
Raised when attempting to return a book that was not borrowed by the member.

---

## Usage Examples

### Basic Example

```python
from library_system import Library, Book, Member, BookCategory

# Create library
library = Library("My Library")

# Add a book
book = Book("1984", "George Orwell", "9780451524935", BookCategory.FICTION, 1949)
library.add_book(book)

# Add a member
member = Member("John Doe", "john@example.com", "M001")
library.add_member(member)

# Borrow a book
member.borrow_book(book)

# Return a book
member.return_book(book)
```

### Advanced Example with Persistence

```python
from pathlib import Path
from library_system import Library, Book, Member
from library_system.services import StorageService
from library_system.config import Settings

# Load settings
settings = Settings.load_or_default(Path("config/library_config.json"))

# Create storage service
storage = StorageService(Path(settings.storage_path))

# Load or create library
library = storage.load_library() or Library(settings.library_name)

# ... perform operations ...

# Save library
storage.save_library(library)
```
