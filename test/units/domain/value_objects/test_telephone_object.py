import pytest

from src.domain.entities.exceptions import InvalidPhoneError
from src.domain.entities.value_objects import Telephone


def test_invalid_telephone():
    invalid_numbers = [
        "dffs",
        "+33",
        "0245787",
        "0245.78",
        "0214587745455166448487451",
        "0015457845"
    ]

    for number in invalid_numbers:
        with pytest.raises(InvalidPhoneError):
            Telephone(number)


def test_valid_telephone():
    valid_numbers = [
        "0269785612",
        "+33678455654",
        "0145784512",
        "05 45 78 45 12",
        "03-45-78-56-78",
        "+33880080000"
    ]

    for number in valid_numbers:
        telephone = Telephone(number)
        assert isinstance(telephone, Telephone)