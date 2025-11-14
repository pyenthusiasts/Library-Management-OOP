"""
Library Management System

A comprehensive library management system demonstrating OOP principles in Python.
"""

__version__ = "2.0.0"
__author__ = "Library Management Team"

from .models import Person, Member, Book, BookCategory, Library
from .exceptions import (
    LibraryException,
    BookNotAvailableError,
    BookNotFoundError,
    MemberNotFoundError,
    InvalidISBNError,
    InvalidEmailError,
)
from .services import StorageService
from .config import Settings

__all__ = [
    "Person",
    "Member",
    "Book",
    "BookCategory",
    "Library",
    "LibraryException",
    "BookNotAvailableError",
    "BookNotFoundError",
    "MemberNotFoundError",
    "InvalidISBNError",
    "InvalidEmailError",
    "StorageService",
    "Settings",
]
