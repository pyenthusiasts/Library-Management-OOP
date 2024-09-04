# Library Management System - OOP Example

This project demonstrates an advanced Python implementation of a **Library Management System** using Object-Oriented Programming (OOP) principles. The system manages books and members, allowing for operations such as borrowing and returning books. It showcases key OOP concepts like inheritance, encapsulation, polymorphism, abstraction, and composition.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Examples](#examples)
6. [Contributing](#contributing)
7. [License](#license)

## Introduction

The Library Management System is a simple application designed to manage a collection of books and a list of members. Members can borrow and return books, and the system keeps track of which books are currently borrowed. This project serves as a practical example of how to design and implement a system using OOP principles in Python.

## Features

- **Abstract Base Class (`Person`)**: Defines a common interface for all persons in the system.
- **Inheritance**: The `Member` class inherits from the `Person` class and extends its functionality.
- **Encapsulation**: Private attributes are used to protect sensitive data and control access.
- **Polymorphism**: Methods with the same name can behave differently depending on the object that invokes them.
- **Composition**: The `Library` class manages collections of `Book` and `Member` objects.
- **Book Management**: Add, list, borrow, and return books.
- **Member Management**: Add members, list members, and manage their borrowed books.

## Installation

### Prerequisites

- Python 3.x

### Install Required Packages

No external packages are required for this project.

## Usage

1. **Clone the Repository**:

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/library-management-system.git
   ```

2. **Navigate to the Directory**:

   Go to the project directory:

   ```bash
   cd library-management-system
   ```

3. **Run the Script**:

   Run the script using Python:

   ```bash
   python library_management_system.py
   ```

### Running the Program

When you run the script, it will:

- Create a library and add a few books and members.
- Perform various operations like borrowing and returning books.
- Display the list of books and members before and after operations.

## Examples

### Output

Running the script will produce output similar to:

```
Added book: The Great Gatsby.
Added book: To Kill a Mockingbird.
Added book: 1984.
Added member: Alice Johnson.
Added member: Bob Smith.

=== List of Books ===
Title: The Great Gatsby, Author: F. Scott Fitzgerald, ISBN: 9780743273565
Title: To Kill a Mockingbird, Author: Harper Lee, ISBN: 9780061120084
Title: 1984, Author: George Orwell, ISBN: 9780451524935

=== List of Members ===
Member ID: M001, Name: Alice Johnson, Email: alice.j@example.com
Member ID: M002, Name: Bob Smith, Email: bob.s@example.com

Alice Johnson borrowed 'The Great Gatsby'.
Bob Smith borrowed 'To Kill a Mockingbird'.

=== List of Available Books ===
Title: 1984, Author: George Orwell, ISBN: 9780451524935

Alice Johnson returned 'The Great Gatsby'.

=== List of Available Books ===
Title: The Great Gatsby, Author: F. Scott Fitzgerald, ISBN: 9780743273565
Title: 1984, Author: George Orwell, ISBN: 9780451524935
```

### Extending the System

To extend the system, you can:

- **Add more features**: Implement more functionality like reserving books, tracking due dates, or generating reports.
- **Create new types of users**: Implement different types of members (e.g., students, faculty) with specific rules.
- **Enhance the UI**: Develop a command-line or graphical interface to interact with the system.

## Contributing

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, please feel free to open an issue or create a pull request.

### Steps to Contribute

1. **Fork the Repository**: Click the 'Fork' button at the top right of this page.
2. **Clone Your Fork**: Clone your forked repository to your local machine.
   ```bash
   git clone https://github.com/your-username/library-management-system.git
   ```
3. **Create a Branch**: Create a new branch for your feature or bug fix.
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make Changes**: Make your changes and commit them with a descriptive message.
   ```bash
   git commit -m "Add: feature description"
   ```
5. **Push Changes**: Push your changes to your forked repository.
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request**: Go to the original repository on GitHub and create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for using the Library Management System! If you have any questions or feedback, feel free to reach out. Happy coding! 📚
