"""Unit tests for the StorageService."""

import pytest
from pathlib import Path
import tempfile
import shutil

from library_system.models import Library, Book, Member, BookCategory
from library_system.services import StorageService


class TestStorageService:
    """Test cases for the StorageService class."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def storage_service(self, temp_dir):
        """Create a StorageService instance for testing."""
        storage_path = temp_dir / "test_library.json"
        return StorageService(storage_path)

    @pytest.fixture
    def sample_library(self):
        """Create a sample library for testing."""
        library = Library("Test Library")

        # Add books
        book1 = Book("Book 1", "Author 1", "9780743273565", BookCategory.FICTION, 2020)
        book2 = Book("Book 2", "Author 2", "9780061120084", BookCategory.SCIENCE, 2019)
        library.add_book(book1)
        library.add_book(book2)

        # Add members
        member1 = Member("John Doe", "john@example.com", "M001")
        member2 = Member("Jane Doe", "jane@example.com", "M002")
        library.add_member(member1)
        library.add_member(member2)

        # Borrow a book
        member1.borrow_book(book1)

        return library

    def test_save_library(self, storage_service, sample_library):
        """Test saving library data."""
        storage_service.save_library(sample_library)

        assert storage_service.storage_exists()

    def test_load_library(self, storage_service, sample_library):
        """Test loading library data."""
        storage_service.save_library(sample_library)
        loaded_library = storage_service.load_library()

        assert loaded_library is not None
        assert loaded_library.name == "Test Library"
        assert len(loaded_library.get_all_books()) == 2
        assert len(loaded_library.get_all_members()) == 2

    def test_load_nonexistent_library(self, storage_service):
        """Test loading when no data file exists."""
        loaded_library = storage_service.load_library()

        assert loaded_library is None

    def test_load_save_preserves_borrowing(self, storage_service, sample_library):
        """Test that borrowing relationships are preserved."""
        storage_service.save_library(sample_library)
        loaded_library = storage_service.load_library()

        # Check that the book is still borrowed
        book = loaded_library.get_book("9780743273565")
        assert not book.is_available()

        # Check that the member has the borrowed book
        member = loaded_library.get_member("M001")
        assert len(member.get_borrowed_books()) == 1

    def test_delete_storage(self, storage_service, sample_library):
        """Test deleting the storage file."""
        storage_service.save_library(sample_library)
        assert storage_service.storage_exists()

        storage_service.delete_storage()
        assert not storage_service.storage_exists()

    def test_storage_exists(self, storage_service):
        """Test checking if storage exists."""
        assert not storage_service.storage_exists()

        library = Library("Test Library")
        storage_service.save_library(library)

        assert storage_service.storage_exists()
