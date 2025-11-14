"""Storage service for persisting library data."""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime

from ..models import Library, Book, Member, BookCategory


class StorageService:
    """
    Service for saving and loading library data to/from JSON files.

    This service handles the serialization and deserialization of library
    data, allowing the library state to be persisted between sessions.
    """

    def __init__(self, storage_path: Optional[Path] = None) -> None:
        """
        Initialize the StorageService.

        Args:
            storage_path: The path where library data will be stored.
                         If None, defaults to './data/library_data.json'.
        """
        if storage_path is None:
            storage_path = Path("data/library_data.json")

        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def save_library(self, library: Library) -> None:
        """
        Save the library data to a JSON file.

        Args:
            library: The library instance to save.

        Raises:
            IOError: If there's an error writing to the file.
        """
        data = library.to_dict()

        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise IOError(f"Failed to save library data: {e}")

    def load_library(self) -> Optional[Library]:
        """
        Load library data from a JSON file.

        Returns:
            A Library instance with the loaded data, or None if the file doesn't exist.

        Raises:
            IOError: If there's an error reading from the file.
            ValueError: If the data is invalid.
        """
        if not self.storage_path.exists():
            return None

        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except IOError as e:
            raise IOError(f"Failed to load library data: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {e}")

        return self._deserialize_library(data)

    def _deserialize_library(self, data: dict) -> Library:
        """
        Deserialize library data from a dictionary.

        Args:
            data: The dictionary containing library data.

        Returns:
            A Library instance.
        """
        library = Library(name=data.get("name", "Library"))

        # Restore books
        books_data = data.get("books", [])
        books_dict = {}

        for book_data in books_data:
            try:
                category = BookCategory(book_data.get("category", "Other"))
            except ValueError:
                category = BookCategory.OTHER

            book = Book(
                title=book_data["title"],
                author=book_data["author"],
                isbn=book_data["isbn"],
                category=category,
                publication_year=book_data.get("publication_year"),
            )
            books_dict[book.isbn] = book
            library.add_book(book)

        # Restore members
        members_data = data.get("members", [])
        members_dict = {}

        for member_data in members_data:
            member = Member(
                name=member_data["name"],
                email=member_data["email"],
                member_id=member_data["member_id"],
                max_books=member_data.get("max_books", Member.DEFAULT_MAX_BOOKS),
            )

            # Restore membership date
            if "membership_date" in member_data:
                member._membership_date = datetime.fromisoformat(member_data["membership_date"])

            members_dict[member.member_id] = member
            library.add_member(member)

        # Restore borrowing relationships
        for book_data in books_data:
            if not book_data.get("is_available", True):
                borrower_id = book_data.get("borrower_id")
                if borrower_id and borrower_id in members_dict:
                    book = books_dict[book_data["isbn"]]
                    member = members_dict[borrower_id]

                    # Restore the borrowing relationship
                    member._borrowed_books.append(book)
                    book._borrower = member

                    if book_data.get("borrowed_date"):
                        book._borrowed_date = datetime.fromisoformat(book_data["borrowed_date"])
                    if book_data.get("due_date"):
                        book._due_date = datetime.fromisoformat(book_data["due_date"])

        return library

    def delete_storage(self) -> None:
        """
        Delete the storage file.

        Raises:
            IOError: If there's an error deleting the file.
        """
        if self.storage_path.exists():
            try:
                self.storage_path.unlink()
            except IOError as e:
                raise IOError(f"Failed to delete storage file: {e}")

    def storage_exists(self) -> bool:
        """
        Check if the storage file exists.

        Returns:
            True if the storage file exists, False otherwise.
        """
        return self.storage_path.exists()
