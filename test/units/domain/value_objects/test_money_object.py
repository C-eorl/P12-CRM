import pytest

from src.domain.entities.exceptions import InvalidAmountError
from src.domain.entities.value_objects import Money


def test_valid_money():
    valid_amounts = [
        "4564",
        "125.45",
        45,
        12.2,
        45.45,
        448.456
    ]
    for amount in valid_amounts:
            money = Money(amount)
            assert isinstance(money, Money)

def test_invalid_amount():
    invalid_amounts = [
        "dfs",
        "12.sd"
    ]
    for amount in invalid_amounts:
        with pytest.raises(InvalidAmountError):
            Money(amount)