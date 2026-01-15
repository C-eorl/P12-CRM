import re
from dataclasses import dataclass
from decimal import Decimal

from src.domain.entities.exceptions import InvalidPhoneError, InvalidEmailError, InvalidAmountError


@dataclass(frozen=True)
class Money:
    amount: Decimal

    def __post_init__(self):
        try:
            amount = Decimal(str(self.amount))
        except Exception:
            raise InvalidAmountError("Montant invalide")

        if amount < Decimal("0"):
            raise InvalidAmountError("Le montant ne peut pas être négatif")

        object.__setattr__(self, "amount", amount)

    def __str__(self):
        return f"{self.amount:.2f}"

    def __add__(self, other):
        if not isinstance(other, Money):
            raise TypeError("Opération valide qu'entre Money")
        return Money(self.amount + other.amount)

    def __sub__(self, other):
        if not isinstance(other, Money):
            raise TypeError("Opération valide qu'entre Money")
        result = self.amount - other.amount
        if result < 0:
            raise InvalidAmountError("Le montant ne peut pas être négatif")
        return Money(result)

    def __lt__(self, other):
        if not isinstance(other, Money):
            raise TypeError("Comparaison impossible")
        return self.amount < other.amount

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
        pattern = r'^(?:\+33|0)[1-9](?:[\s\-]?\d{2}){4}$'

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