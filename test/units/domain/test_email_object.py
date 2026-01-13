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
    email1 = Email("test@test.fr")
    email2 = Email("john.test.41@mail.com")
    email3 = Email("a_4_test@sub.mail.com")

    assert isinstance(email1, Email)
    assert isinstance(email2, Email)
    assert isinstance(email3, Email)