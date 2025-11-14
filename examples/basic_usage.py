"""
Basic usage example for the library management system.

This example demonstrates the fundamental operations:
- Creating a library
- Adding books and members
- Borrowing and returning books
"""

from library_system import Library, Book, Member, BookCategory

def main():
    # Create a library
    library = Library("City Public Library")
    print(f"Created: {library.name}\n")

    # Add some books
    print("Adding books to the library...")
    book1 = Book(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        isbn="9780743273565",
        category=BookCategory.FICTION,
        publication_year=1925
    )
    book2 = Book(
        title="To Kill a Mockingbird",
        author="Harper Lee",
        isbn="9780061120084",
        category=BookCategory.FICTION,
        publication_year=1960
    )
    book3 = Book(
        title="1984",
        author="George Orwell",
        isbn="9780451524935",
        category=BookCategory.FICTION,
        publication_year=1949
    )

    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)
    print(f"Added {len(library.get_all_books())} books\n")

    # Add members
    print("Adding members...")
    member1 = Member("Alice Johnson", "alice.j@example.com", "M001")
    member2 = Member("Bob Smith", "bob.s@example.com", "M002")

    library.add_member(member1)
    library.add_member(member2)
    print(f"Added {len(library.get_all_members())} members\n")

    # Display all books
    print("=== Available Books ===")
    for book in library.get_available_books():
        print(f"  {book}")
    print()

    # Member borrows a book
    print("Alice borrows 'The Great Gatsby'...")
    member1.borrow_book(book1)
    print(f"  Borrowed successfully!")
    print(f"  Due date: {book1.due_date.strftime('%Y-%m-%d')}\n")

    # Display available books after borrowing
    print("=== Available Books (After Borrowing) ===")
    for book in library.get_available_books():
        print(f"  {book}")
    print()

    # Display member details
    print("=== Member Details ===")
    for member in library.get_all_members():
        print(f"  {member.get_details()}")
    print()

    # Return a book
    print("Alice returns 'The Great Gatsby'...")
    member1.return_book(book1)
    print(f"  Returned successfully!\n")

    # Display statistics
    print("=== Library Statistics ===")
    stats = library.get_statistics()
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")


if __name__ == "__main__":
    main()
