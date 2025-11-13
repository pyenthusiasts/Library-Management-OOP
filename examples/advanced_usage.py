"""
Advanced usage example for the library management system.

This example demonstrates advanced features:
- Data persistence with JSON storage
- Search functionality
- Late fees calculation
- Configuration management
"""

from pathlib import Path
from datetime import datetime, timedelta

from library_system import Library, Book, Member, BookCategory
from library_system.services import StorageService
from library_system.config import Settings

def main():
    # Load or create settings
    settings = Settings(
        library_name="Advanced Library System",
        max_books_per_member=3,
        loan_period_days=7,
        late_fee_per_day=1.00,
        storage_path="data/advanced_library.json"
    )

    # Create storage service
    storage = StorageService(Path(settings.storage_path))

    # Try to load existing library or create new one
    library = storage.load_library()
    if library is None:
        print("Creating new library...")
        library = Library(settings.library_name)

        # Add books from different categories
        books_data = [
            ("The Hobbit", "J.R.R. Tolkien", "9780547928227", BookCategory.FANTASY, 1937),
            ("Sapiens", "Yuval Noah Harari", "9780062316097", BookCategory.HISTORY, 2011),
            ("The Selfish Gene", "Richard Dawkins", "9780198788607", BookCategory.SCIENCE, 1976),
            ("Clean Code", "Robert C. Martin", "9780132350884", BookCategory.TECHNOLOGY, 2008),
            ("Becoming", "Michelle Obama", "9781524763138", BookCategory.BIOGRAPHY, 2018),
        ]

        for title, author, isbn, category, year in books_data:
            book = Book(title, author, isbn, category, year)
            library.add_book(book)

        # Add members
        members_data = [
            ("Emma Wilson", "emma.w@example.com", "M001"),
            ("Michael Chen", "michael.c@example.com", "M002"),
            ("Sarah Davis", "sarah.d@example.com", "M003"),
        ]

        for name, email, member_id in members_data:
            member = Member(name, email, member_id, settings.max_books_per_member)
            library.add_member(member)

        print(f"Created library with {len(library.get_all_books())} books and {len(library.get_all_members())} members\n")
    else:
        print(f"Loaded existing library: {library.name}\n")

    # Demonstrate search functionality
    print("=== Search Books by Category: SCIENCE ===")
    science_books = library.find_books_by_category(BookCategory.SCIENCE)
    for book in science_books:
        print(f"  {book}")
    print()

    print("=== Search Books by Author: 'Obama' ===")
    obama_books = library.find_books_by_author("Obama")
    for book in obama_books:
        print(f"  {book}")
    print()

    # Borrow books
    member = library.get_member("M001")
    available_books = library.get_available_books()

    if len(available_books) >= 2:
        print(f"=== {member.name} borrows 2 books ===")
        member.borrow_book(available_books[0])
        print(f"  Borrowed: {available_books[0].title}")
        member.borrow_book(available_books[1])
        print(f"  Borrowed: {available_books[1].title}")
        print()

        # Simulate overdue scenario
        print("=== Simulating Overdue Scenario ===")
        # Make one book overdue by 5 days
        overdue_book = available_books[0]
        overdue_book._due_date = datetime.now() - timedelta(days=5)

        print(f"Made '{overdue_book.title}' overdue by 5 days\n")

        # Check overdue books
        print("=== Overdue Books ===")
        overdue_books = library.get_overdue_books()
        for book in overdue_books:
            days_overdue = book.days_overdue()
            late_fee = days_overdue * settings.late_fee_per_day
            print(f"  '{book.title}' - {days_overdue} days overdue")
            print(f"    Borrowed by: {book.borrower.name}")
            print(f"    Late fee: ${late_fee:.2f}")
        print()

        # Calculate member's total late fees
        member_fees = member.calculate_late_fees(settings.late_fee_per_day)
        print(f"Total late fees for {member.name}: ${member_fees:.2f}\n")

    # Display library statistics
    print("=== Library Statistics ===")
    stats = library.get_statistics()
    print(f"  Library: {library.name}")
    print(f"  Total Books: {stats['total_books']}")
    print(f"  Available: {stats['available_books']}")
    print(f"  Borrowed: {stats['borrowed_books']}")
    print(f"  Overdue: {stats['overdue_books']}")
    print(f"  Total Members: {stats['total_members']}")
    print(f"  Members with Overdue: {stats['members_with_overdue']}")
    print()

    # Save library data
    print("Saving library data...")
    storage.save_library(library)
    print(f"Data saved to: {storage.storage_path}")
    print("\nYou can run this script again to see persistence in action!")


if __name__ == "__main__":
    main()
