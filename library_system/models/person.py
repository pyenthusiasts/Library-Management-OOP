"""Abstract base class for persons in the library system."""

from abc import ABC, abstractmethod
from ..exceptions import InvalidEmailError
from ..utils import validate_email


class Person(ABC):
    """
    Abstract base class representing a person.

    This class provides a common interface and shared functionality
    for all person types in the library system.

    Attributes:
        name: The name of the person.
        email: The email address of the person.
    """

    def __init__(self, name: str, email: str) -> None:
        """
        Initialize a Person instance.

        Args:
            name: The name of the person.
            email: The email address of the person.

        Raises:
            InvalidEmailError: If the email address is invalid.
        """
        if not validate_email(email):
            raise InvalidEmailError(email)

        self._name = name
        self._email = email

    @property
    def name(self) -> str:
        """Get the person's name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the person's name."""
        self._name = value

    @property
    def email(self) -> str:
        """Get the person's email."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """
        Set the person's email.

        Args:
            value: The new email address.

        Raises:
            InvalidEmailError: If the email address is invalid.
        """
        if not validate_email(value):
            raise InvalidEmailError(value)
        self._email = value

    @abstractmethod
    def get_details(self) -> str:
        """
        Get the details of the person.

        Returns:
            A string representation of the person's details.
        """
        pass

    def __repr__(self) -> str:
        """Return a string representation of the person."""
        return f"{self.__class__.__name__}(name='{self.name}', email='{self.email}')"
