from typing import List

from sqlalchemy import select

from src.domain.entities.entities import User
from src.infrastructures.database.models import UserModel


def test_save_user_create(user_SQLAlchemy_repository, user_support, session):
    init_count_user = session.query(UserModel).count()
    saved_user = user_SQLAlchemy_repository.save(user_support)
    current_count_user = session.query(UserModel).count()
    assert isinstance(saved_user, User)
    assert init_count_user + 1 == current_count_user

def test_save_user_update(user_SQLAlchemy_repository):
    """test save method for update client"""
    saved_user = user_SQLAlchemy_repository.find_by_id(7)

    saved_user.fullname = "modify test"
    user_SQLAlchemy_repository.save(saved_user)

    updated_user = user_SQLAlchemy_repository.find_by_id(7)
    assert updated_user.fullname == "modify test"
    assert saved_user.email == updated_user.email

def test_find_by_id(user_SQLAlchemy_repository):
    """test find by id method """
    user_find = user_SQLAlchemy_repository.find_by_id(6)

    assert isinstance(user_find, User)
    assert user_find.email.address == "francois.petit@example.com"

def test_find_by_invalid_id(user_SQLAlchemy_repository):
    """test find all method """
    find_user = user_SQLAlchemy_repository.find_by_id(45)

    assert find_user is None

def test_find_all(user_SQLAlchemy_repository, session):
    """test find all method """
    all_users = user_SQLAlchemy_repository.find_all()

    assert isinstance(all_users, List)
    actual_count_user = session.query(UserModel).count()
    assert len(all_users) == actual_count_user

def test_find_by_email(user_SQLAlchemy_repository):
    """test find by email method """
    user_find = user_SQLAlchemy_repository.find_by_email("francois.petit@example.com")

    assert isinstance(user_find, User)
    assert user_find.id == 6

def test_find_by_invalid_email(user_SQLAlchemy_repository):
    """test find by invalid email method """
    user_find = user_SQLAlchemy_repository.find_by_email("invalid_email@dd.fr")

    assert user_find is None

def test_find_by_role(user_SQLAlchemy_repository, session):
    """test find by role method """
    users_find = user_SQLAlchemy_repository.find_by_role("SUPPORT")

    assert isinstance(users_find, List)
    actual_count_user = session.query(UserModel).where(UserModel.role == "SUPPORT").count()
    assert len(users_find) == actual_count_user


def test_delete(user_SQLAlchemy_repository, session, user_commercial):
    """test delete method """
    init_count_user = session.query(UserModel).count()
    user_SQLAlchemy_repository.save(user_commercial)
    session.commit()
    last_user = session.execute(select(UserModel)).scalars().all()[-1]
    delete_user = user_SQLAlchemy_repository.delete(last_user.id)

    assert delete_user is None
    actual_count_user = session.query(UserModel).count()
    assert actual_count_user == init_count_user