"""Command-line interface for the library management system."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from ..models import Library, Book, Member, BookCategory
from ..services import StorageService
from ..config import Settings
from ..exceptions import LibraryException


class LibraryCLI:
    """Command-line interface for the library management system."""

    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize the CLI.

        Args:
            settings: Configuration settings. If None, default settings are used.
        """
        self.settings = settings or Settings()
        self.storage = StorageService(Path(self.settings.storage_path))
        self.library = self._load_or_create_library()

    def _load_or_create_library(self) -> Library:
        """Load existing library data or create a new library."""
        if self.storage.storage_exists():
            try:
                library = self.storage.load_library()
                if library:
                    print(f"Loaded existing library: {library.name}")
                    return library
            except Exception as e:
                print(f"Error loading library data: {e}")

        print(f"Creating new library: {self.settings.library_name}")
        return Library(name=self.settings.library_name)

    def save_library(self) -> None:
        """Save the current library state."""
        try:
            self.storage.save_library(self.library)
            print("Library data saved successfully.")
        except Exception as e:
            print(f"Error saving library data: {e}")

    def add_book_interactive(self) -> None:
        """Interactively add a book to the library."""
        print("\n=== Add New Book ===")
        title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()
        isbn = input("Enter ISBN: ").strip()

        print("\nAvailable categories:")
        for i, cat in enumerate(BookCategory, 1):
            print(f"{i}. {cat.value}")

        cat_choice = input("Select category (number): ").strip()
        try:
            category = list(BookCategory)[int(cat_choice) - 1]
        except (ValueError, IndexError):
            category = BookCategory.OTHER
            print("Invalid choice. Using 'Other' category.")

        year_input = input("Enter publication year (optional): ").strip()
        year = int(year_input) if year_input.isdigit() else None

        try:
            book = Book(title, author, isbn, category, year)
            self.library.add_book(book)
            print(f"\nSuccessfully added: {book}")
            self.save_library()
        except LibraryException as e:
            print(f"\nError: {e}")

    def add_member_interactive(self) -> None:
        """Interactively add a member to the library."""
        print("\n=== Add New Member ===")
        name = input("Enter member name: ").strip()
        email = input("Enter email address: ").strip()
        member_id = input("Enter member ID: ").strip()

        try:
            member = Member(name, email, member_id, self.settings.max_books_per_member)
            self.library.add_member(member)
            print(f"\nSuccessfully added: {member}")
            self.save_library()
        except LibraryException as e:
            print(f"\nError: {e}")

    def borrow_book_interactive(self) -> None:
        """Interactively borrow a book."""
        print("\n=== Borrow Book ===")
        member_id = input("Enter member ID: ").strip()
        isbn = input("Enter book ISBN: ").strip()

        try:
            member = self.library.get_member(member_id)
            book = self.library.get_book(isbn)
            member.borrow_book(book)
            print(f"\n{member.name} borrowed '{book.title}'")
            print(f"Due date: {book.due_date.strftime('%Y-%m-%d')}")
            self.save_library()
        except LibraryException as e:
            print(f"\nError: {e}")

    def return_book_interactive(self) -> None:
        """Interactively return a book."""
        print("\n=== Return Book ===")
        member_id = input("Enter member ID: ").strip()
        isbn = input("Enter book ISBN: ").strip()

        try:
            member = self.library.get_member(member_id)
            book = self.library.get_book(isbn)
            member.return_book(book)

            late_fees = 0.0
            if book.days_overdue() > 0:
                late_fees = book.days_overdue() * self.settings.late_fee_per_day
                print(f"\nBook was {book.days_overdue()} days overdue.")
                print(f"Late fee: ${late_fees:.2f}")

            print(f"\n{member.name} returned '{book.title}'")
            self.save_library()
        except LibraryException as e:
            print(f"\nError: {e}")

    def list_books(self, available_only: bool = False) -> None:
        """List all books or only available books."""
        books = self.library.get_available_books() if available_only else self.library.get_all_books()

        if not books:
            print("\nNo books found.")
            return

        status = "Available Books" if available_only else "All Books"
        print(f"\n=== {status} ===")
        for book in sorted(books, key=lambda b: b.title):
            print(f"  {book}")

    def list_members(self) -> None:
        """List all members."""
        members = self.library.get_all_members()

        if not members:
            print("\nNo members found.")
            return

        print("\n=== All Members ===")
        for member in sorted(members, key=lambda m: m.name):
            print(f"  {member.get_details()}")

    def search_books(self) -> None:
        """Search for books."""
        print("\n=== Search Books ===")
        print("1. Search by title")
        print("2. Search by author")
        print("3. Search by category")

        choice = input("Select search type: ").strip()

        if choice == "1":
            title = input("Enter title to search: ").strip()
            books = self.library.find_books_by_title(title)
        elif choice == "2":
            author = input("Enter author to search: ").strip()
            books = self.library.find_books_by_author(author)
        elif choice == "3":
            print("\nAvailable categories:")
            for i, cat in enumerate(BookCategory, 1):
                print(f"{i}. {cat.value}")
            cat_choice = input("Select category (number): ").strip()
            try:
                category = list(BookCategory)[int(cat_choice) - 1]
                books = self.library.find_books_by_category(category)
            except (ValueError, IndexError):
                print("Invalid choice.")
                return
        else:
            print("Invalid choice.")
            return

        if not books:
            print("\nNo books found.")
            return

        print(f"\nFound {len(books)} book(s):")
        for book in books:
            print(f"  {book}")

    def show_statistics(self) -> None:
        """Display library statistics."""
        stats = self.library.get_statistics()

        print("\n=== Library Statistics ===")
        print(f"Library Name: {self.library.name}")
        print(f"Total Books: {stats['total_books']}")
        print(f"  Available: {stats['available_books']}")
        print(f"  Borrowed: {stats['borrowed_books']}")
        print(f"  Overdue: {stats['overdue_books']}")
        print(f"Total Members: {stats['total_members']}")
        print(f"  With Overdue Books: {stats['members_with_overdue']}")

    def show_overdue(self) -> None:
        """Show overdue books and members."""
        overdue_books = self.library.get_overdue_books()

        if not overdue_books:
            print("\nNo overdue books.")
            return

        print("\n=== Overdue Books ===")
        for book in overdue_books:
            days_overdue = book.days_overdue()
            late_fee = days_overdue * self.settings.late_fee_per_day
            print(f"  '{book.title}' - Borrowed by {book.borrower.name}")
            print(f"    Due: {book.due_date.strftime('%Y-%m-%d')}")
            print(f"    Days Overdue: {days_overdue}")
            print(f"    Late Fee: ${late_fee:.2f}")

    def run_interactive(self) -> None:
        """Run the interactive CLI."""
        print(f"\n{'='*50}")
        print(f"  {self.library.name} - Management System")
        print(f"{'='*50}")

        while True:
            print("\n=== Main Menu ===")
            print("1. Add Book")
            print("2. Add Member")
            print("3. Borrow Book")
            print("4. Return Book")
            print("5. List All Books")
            print("6. List Available Books")
            print("7. List Members")
            print("8. Search Books")
            print("9. Show Statistics")
            print("10. Show Overdue Books")
            print("0. Exit")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                self.add_book_interactive()
            elif choice == "2":
                self.add_member_interactive()
            elif choice == "3":
                self.borrow_book_interactive()
            elif choice == "4":
                self.return_book_interactive()
            elif choice == "5":
                self.list_books(available_only=False)
            elif choice == "6":
                self.list_books(available_only=True)
            elif choice == "7":
                self.list_members()
            elif choice == "8":
                self.search_books()
            elif choice == "9":
                self.show_statistics()
            elif choice == "10":
                self.show_overdue()
            elif choice == "0":
                self.save_library()
                print("\nGoodbye!")
                break
            else:
                print("\nInvalid choice. Please try again.")


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Library Management System - Command Line Interface"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration file",
        default=None,
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run with demo data",
    )

    args = parser.parse_args()

    # Load settings
    settings = Settings.load_or_default(args.config)

    # Create CLI instance
    cli = LibraryCLI(settings)

    # Add demo data if requested
    if args.demo:
        try:
            # Add sample books
            cli.library.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", BookCategory.FICTION, 1925))
            cli.library.add_book(Book("To Kill a Mockingbird", "Harper Lee", "9780061120084", BookCategory.FICTION, 1960))
            cli.library.add_book(Book("1984", "George Orwell", "9780451524935", BookCategory.FICTION, 1949))
            cli.library.add_book(Book("A Brief History of Time", "Stephen Hawking", "9780553380163", BookCategory.SCIENCE, 1988))

            # Add sample members
            cli.library.add_member(Member("Alice Johnson", "alice.j@example.com", "M001"))
            cli.library.add_member(Member("Bob Smith", "bob.s@example.com", "M002"))

            print("Demo data loaded successfully!")
            cli.save_library()
        except Exception as e:
            print(f"Note: {e}")

    # Run interactive mode
    try:
        cli.run_interactive()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Saving data...")
        cli.save_library()
        sys.exit(0)


if __name__ == "__main__":
    main()
