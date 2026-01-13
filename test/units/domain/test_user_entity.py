from src.domain.entities.entities import User
from src.domain.entities.enums import Role
from src.domain.entities.value_objects import Email

def test_user_create():
    user = User(id=1, full_name="test test",
                email=Email("test@test.com"), password="sfsefs",
                role=Role.COMMERCIAL)

    assert type(user.id) == int
    assert type(user.full_name) == str
    assert type(user.email) == Email
    assert type(user.password) == str
    assert type(user.role) == Role

def test_user_is_commercial():
    user = User(id=1, full_name="test test",
         email=Email("test@test.com"), password="sfsefs",
         role=Role.COMMERCIAL)

    assert user.is_commercial() is True
    assert user.is_support() is False
    assert user.is_gestion() is False

def test_user_is_support():
    user = User(id=1, full_name="test test",
         email=Email("test@test.com"), password="sfsefs",
         role=Role.SUPPORT)

    assert user.is_commercial() is False
    assert user.is_support() is True
    assert user.is_gestion() is False

def test_user_is_gestion():
    user = User(id=1, full_name="test test",
         email=Email("test@test.com"), password="sfsefs",
         role=Role.GESTION)

    assert user.is_commercial() is False
    assert user.is_support() is False
    assert user.is_gestion() is True

