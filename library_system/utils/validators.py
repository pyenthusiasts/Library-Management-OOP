"""Validation utilities for the library management system."""

import re
from typing import bool


def validate_email(email: str) -> bool:
    """
    Validate an email address.

    Args:
        email: The email address to validate.

    Returns:
        True if the email is valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_isbn(isbn: str) -> bool:
    """
    Validate an ISBN-10 or ISBN-13 number.

    Args:
        isbn: The ISBN to validate.

    Returns:
        True if the ISBN is valid, False otherwise.
    """
    # Remove hyphens and spaces
    isbn = isbn.replace("-", "").replace(" ", "")

    # Check ISBN-10
    if len(isbn) == 10:
        if not isbn[:-1].isdigit():
            return False
        if isbn[-1] not in '0123456789X':
            return False
        return _validate_isbn10(isbn)

    # Check ISBN-13
    elif len(isbn) == 13:
        if not isbn.isdigit():
            return False
        return _validate_isbn13(isbn)

    return False


def _validate_isbn10(isbn: str) -> bool:
    """Validate ISBN-10 checksum."""
    total = 0
    for i, digit in enumerate(isbn[:-1]):
        total += int(digit) * (10 - i)

    check_digit = isbn[-1]
    if check_digit == 'X':
        total += 10
    else:
        total += int(check_digit)

    return total % 11 == 0


def _validate_isbn13(isbn: str) -> bool:
    """Validate ISBN-13 checksum."""
    total = 0
    for i, digit in enumerate(isbn[:-1]):
        multiplier = 1 if i % 2 == 0 else 3
        total += int(digit) * multiplier

    check_digit = (10 - (total % 10)) % 10
    return check_digit == int(isbn[-1])
