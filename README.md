# Library Management System 2.0

[![CI](https://github.com/pyenthusiasts/Library-Management-OOP/actions/workflows/ci.yml/badge.svg)](https://github.com/pyenthusiasts/Library-Management-OOP/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive, production-ready library management system demonstrating advanced Object-Oriented Programming (OOP) principles in Python. This project showcases professional software development practices including modular architecture, comprehensive testing, type safety, and modern Python tooling.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [OOP Principles](#oop-principles-demonstrated)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Features
- **Book Management**: Add, remove, search, and categorize books
- **Member Management**: Register members with customizable borrowing limits
- **Borrowing System**: Track book loans with due dates
- **Overdue Tracking**: Automatic overdue detection with late fee calculation
- **Search Functionality**: Search by title, author, or category
- **Data Persistence**: Save and load library state using JSON storage
- **Statistics**: Comprehensive library statistics and reports

### Advanced Features
- **Type Safety**: Full type hints throughout the codebase
- **Custom Exceptions**: Specific exception handling for different error scenarios
- **Data Validation**: Email and ISBN validation
- **Configurable Settings**: JSON-based configuration system
- **CLI Interface**: Interactive command-line interface
- **Extensible Architecture**: Modular design for easy extension

### Developer Features
- **Comprehensive Testing**: Full test coverage with pytest
- **CI/CD Pipeline**: GitHub Actions for automated testing
- **Code Quality Tools**: Black, isort, flake8, mypy, pylint
- **Pre-commit Hooks**: Automated code quality checks
- **API Documentation**: Detailed API reference in `docs/API.md`

## Architecture

The system follows a **layered architecture** with clear separation of concerns:

```
library_system/
├── models/          # Domain models (Book, Member, Library)
├── services/        # Business logic and data persistence
├── exceptions/      # Custom exception classes
├── utils/          # Utility functions (validators)
├── config/         # Configuration management
└── cli/            # Command-line interface
```

## Installation

### Prerequisites
- Python 3.8 or higher

### Standard Installation

```bash
# Clone the repository
git clone https://github.com/pyenthusiasts/Library-Management-OOP.git
cd Library-Management-OOP

# Install the package
pip install -e .
```

### Development Installation

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Quick Start

### Using the CLI

```bash
# Run with demo data
library-cli --demo

# Run with custom configuration
library-cli --config config/library_config.json
```

### Using the API

```python
from library_system import Library, Book, Member, BookCategory

# Create a library
library = Library("My Library")

# Add a book
book = Book(
    title="1984",
    author="George Orwell",
    isbn="9780451524935",
    category=BookCategory.FICTION,
    publication_year=1949
)
library.add_book(book)

# Add a member
member = Member("John Doe", "john@example.com", "M001")
library.add_member(member)

# Borrow a book
member.borrow_book(book)
print(f"Due date: {book.due_date}")

# Return a book
member.return_book(book)
```

## Usage

### Command-Line Interface

The CLI provides an interactive menu for managing your library:

```bash
library-cli
```

**Available Operations:**
1. Add Book
2. Add Member
3. Borrow Book
4. Return Book
5. List All Books
6. List Available Books
7. List Members
8. Search Books
9. Show Statistics
10. Show Overdue Books

### Examples

See the `examples/` directory for complete examples:
- `basic_usage.py`: Basic library operations
- `advanced_usage.py`: Advanced features including persistence and search

Run examples:
```bash
python examples/basic_usage.py
python examples/advanced_usage.py
```

### Advanced Usage with Persistence

```python
from pathlib import Path
from library_system import Library
from library_system.services import StorageService
from library_system.config import Settings

# Load configuration
settings = Settings.load_or_default(Path("config/library_config.json"))

# Initialize storage
storage = StorageService(Path(settings.storage_path))

# Load existing library or create new one
library = storage.load_library() or Library(settings.library_name)

# Perform operations...

# Save changes
storage.save_library(library)
```

## Project Structure

```
Library-Management-OOP/
├── library_system/              # Main package
│   ├── models/                  # Data models
│   ├── services/               # Business logic
│   ├── exceptions/             # Custom exceptions
│   ├── utils/                  # Utilities
│   ├── config/                 # Configuration
│   └── cli/                    # Command-line interface
├── tests/                      # Test suite
├── examples/                   # Usage examples
├── docs/                       # Documentation
├── config/                     # Configuration files
├── setup.py                    # Package setup
├── pyproject.toml             # Build configuration
└── README.md                  # This file
```

## OOP Principles Demonstrated

### 1. Abstraction
- **Abstract Base Class**: `Person` defines the interface for all person types
- **Abstract Methods**: `get_details()` must be implemented by subclasses

### 2. Inheritance
- `Member` inherits from `Person`
- Extends functionality while maintaining the base interface

### 3. Encapsulation
- Private attributes with property accessors
- Controlled access to internal state

### 4. Polymorphism
- Multiple classes implement `get_details()` differently
- Common interface for different object types

### 5. Composition
- `Library` manages collections of `Book` and `Member` objects
- Clear "has-a" relationships

### 6. SOLID Principles
- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Extensible through inheritance and composition
- **Liskov Substitution**: Subclasses can replace parent classes
- **Interface Segregation**: Focused interfaces
- **Dependency Inversion**: Depends on abstractions

## Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Code Quality Tools

```bash
# Format code
black library_system tests examples

# Sort imports
isort library_system tests examples

# Lint
flake8 library_system tests --max-line-length=100

# Type check
mypy library_system

# Run all checks
pre-commit run --all-files
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=library_system --cov-report=html

# Run specific tests
pytest tests/test_models/test_book.py
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes with clear commit messages
4. **Add** tests for new functionality
5. **Ensure** all tests pass (`pytest`)
6. **Run** code quality tools (`pre-commit run --all-files`)
7. **Commit** your changes (`git commit -m 'Add amazing feature'`)
8. **Push** to the branch (`git push origin feature/amazing-feature`)
9. **Create** a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add type hints to all functions
- Write docstrings for all public methods
- Maintain test coverage above 90%
- Update documentation for new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Designed for educational purposes to demonstrate OOP principles
- Inspired by real-world library management systems
- Built with modern Python best practices

## Support

If you encounter any issues or have questions:
- **Issues**: [GitHub Issues](https://github.com/pyenthusiasts/Library-Management-OOP/issues)
- **Documentation**: See [`docs/API.md`](docs/API.md)
- **Examples**: Check the `examples/` directory

---

**Version 2.0.0** - A complete rewrite with professional architecture and comprehensive features.
