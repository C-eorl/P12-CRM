from src.domain.entities.enums import Role
from src.domain.entities.value_objects import Email


def test_user_create(user_commercial):

    assert user_commercial.id is None
    assert type(user_commercial.fullname) == str
    assert type(user_commercial.email) == Email
    assert type(user_commercial.password) == str
    assert type(user_commercial.role) == Role

def test_user_is_commercial(user_commercial):

    assert user_commercial.is_commercial() is True
    assert user_commercial.is_support() is False
    assert user_commercial.is_gestion() is False

def test_user_is_support(user_support):

    assert user_support.is_commercial() is False
    assert user_support.is_support() is True
    assert user_support.is_gestion() is False

def test_user_is_gestion(user_gestion):

    assert user_gestion.is_commercial() is False
    assert user_gestion.is_support() is False
    assert user_gestion.is_gestion() is True

