from abc import ABC, abstractmethod

# Abstract base class representing a person
class Person(ABC):
    """
    Abstract base class representing a person.

    Attributes:
    -----------
    name : str
        The name of the person.
    email : str
        The email of the person.
    """

    def __init__(self, name, email):
        self.name = name
        self.email = email

    @abstractmethod
    def get_details(self):
        """Abstract method to return details of the person."""
        pass


# Class representing a member of the library
class Member(Person):
    """
    Class representing a library member, inherited from Person.

    Attributes:
    -----------
    member_id : str
        The unique ID of the library member.
    borrowed_books : list
        A list of books currently borrowed by the member.

    Methods:
    --------
    borrow_book(book)
        Borrows a book from the library.
    return_book(book)
        Returns a borrowed book to the library.
    get_details()
        Returns the details of the library member.
    """

    def __init__(self, name, email, member_id):
        super().__init__(name, email)
        self.member_id = member_id
        self.__borrowed_books = []  # Encapsulated private attribute

    def borrow_book(self, book):
        """Borrows a book if not already borrowed."""
        if book.is_available():
            self.__borrowed_books.append(book)
            book.borrow(self)
            print(f"{self.name} borrowed '{book.title}'.")
        else:
            print(f"'{book.title}' is not available.")

    def return_book(self, book):
        """Returns a borrowed book."""
        if book in self.__borrowed_books:
            self.__borrowed_books.remove(book)
            book.return_book()
            print(f"{self.name} returned '{book.title}'.")
        else:
            print(f"{self.name} did not borrow '{book.title}'.")

    def get_details(self):
        """Returns the details of the library member."""
        return f"Member ID: {self.member_id}, Name: {self.name}, Email: {self.email}"

    def get_borrowed_books(self):
        """Returns a list of borrowed books."""
        return [book.title for book in self.__borrowed_books]


# Class representing a book in the library
class Book:
    """
    Class representing a book in the library.

    Attributes:
    -----------
    title : str
        The title of the book.
    author : str
        The author of the book.
    isbn : str
        The ISBN number of the book.
    borrower : Member or None
        The member who has borrowed the book, if any.

    Methods:
    --------
    is_available()
        Checks if the book is available for borrowing.
    borrow(member)
        Marks the book as borrowed by a member.
    return_book()
        Marks the book as returned.
    """

    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.__borrower = None  # Encapsulated private attribute

    def is_available(self):
        """Checks if the book is available for borrowing."""
        return self.__borrower is None

    def borrow(self, member):
        """Marks the book as borrowed by a member."""
        self.__borrower = member

    def return_book(self):
        """Marks the book as returned."""
        self.__borrower = None

    def get_borrower(self):
        """Returns the member who borrowed the book."""
        return self.__borrower

    def __str__(self):
        """Returns the string representation of the book."""
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}"


# Class representing a library
class Library:
    """
    Class representing the library.

    Attributes:
    -----------
    books : list
        A list of books in the library.
    members : list
        A list of members in the library.

    Methods:
    --------
    add_book(book)
        Adds a book to the library.
    add_member(member)
        Adds a member to the library.
    list_books()
        Lists all books in the library.
    list_available_books()
        Lists all available books in the library.
    list_members()
        Lists all members in the library.
    """

    def __init__(self):
        self.__books = []  # Encapsulated private attribute
        self.__members = []  # Encapsulated private attribute

    def add_book(self, book):
        """Adds a book to the library."""
        self.__books.append(book)
        print(f"Added book: {book.title}.")

    def add_member(self, member):
        """Adds a member to the library."""
        self.__members.append(member)
        print(f"Added member: {member.name}.")

    def list_books(self):
        """Lists all books in the library."""
        print("\n=== List of Books ===")
        for book in self.__books:
            print(book)

    def list_available_books(self):
        """Lists all available books in the library."""
        print("\n=== List of Available Books ===")
        for book in self.__books:
            if book.is_available():
                print(book)

    def list_members(self):
        """Lists all members in the library."""
        print("\n=== List of Members ===")
        for member in self.__members:
            print(member.get_details())


# Main function to demonstrate the Library Management System
def main():
    # Create a library
    library = Library()

    # Create books
    book1 = Book(title="The Great Gatsby", author="F. Scott Fitzgerald", isbn="9780743273565")
    book2 = Book(title="To Kill a Mockingbird", author="Harper Lee", isbn="9780061120084")
    book3 = Book(title="1984", author="George Orwell", isbn="9780451524935")

    # Add books to the library
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)

    # Create members
    member1 = Member(name="Alice Johnson", email="alice.j@example.com", member_id="M001")
    member2 = Member(name="Bob Smith", email="bob.s@example.com", member_id="M002")

    # Add members to the library
    library.add_member(member1)
    library.add_member(member2)

    # List all books and members
    library.list_books()
    library.list_members()

    # Member borrows a book
    member1.borrow_book(book1)
    member2.borrow_book(book2)

    # List available books after borrowing
    library.list_available_books()

    # Member returns a book
    member1.return_book(book1)

    # List available books after returning
    library.list_available_books()


if __name__ == "__main__":
    main()
