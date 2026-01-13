import re
from dataclasses import dataclass

from src.domain.entities.exceptions import InvalidPhoneError, InvalidEmailError


@dataclass(frozen=True)
class Telephone:
    """Object representing a telephone number"""
    number: str

    def __post_init__(self):
        if not self.is_valid(self.number):
            raise InvalidPhoneError(f"Télephone invalide: {self.number}")

    def __str__(self) -> str:
        return self.number

    @staticmethod
    def is_valid(telephone: str)-> bool:
        """Validate telephone format"""
        if not telephone:
            return False
        pattern = r'^\+?[\d\s\-\(\)]{8,20}$'
        return bool(re.match(pattern, telephone))


@dataclass(frozen=True)
class Email:
    """Object representing an email address"""
    address: str

    def __post_init__(self):
        if not self._is_valid(self.address):
            raise InvalidEmailError(f"E-mail invalide: {self.address}")

    def __str__(self) -> str:
        return self.address

    @staticmethod
    def _is_valid(email: str) -> bool:
        """Validate email format"""
        if not email:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@([a-zA-Z-]+\.)+[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))