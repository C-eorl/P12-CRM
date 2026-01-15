import pytest

from src.domain.entities.exceptions import InvalidEmailError
from src.domain.entities.value_objects import Email


def test_invalid_mail():
    invalid_emails = [
        "test",
        "@test",
        "test/test",
        "test@test",
        "test@test,com",
        "test@test.123",
        "test@test.123.xxx",
    ]

    for email in invalid_emails:
        with pytest.raises(InvalidEmailError):
            Email(email)

def test_valid_mail():
    valid_emails = [
        "test@test.fr",
        "john.test.41@mail.com",
        "a_4_test@sub.mail.com"
    ]

    for email in valid_emails:
        email = Email(email)
        assert isinstance(email, Email)