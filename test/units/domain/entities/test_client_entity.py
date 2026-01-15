from datetime import datetime

import pytest

from src.domain.entities.entities import Client, User
from src.domain.entities.enums import Role
from src.domain.entities.value_objects import Email, Telephone

@pytest.fixture
def user_commercial():
    return User(id=1, full_name="test test",
                email=Email("test@test.com"), password="sfsefs",
                role=Role.COMMERCIAL)

@pytest.fixture
def client(user_commercial):
    return Client(
        id=1,fullname="test test", email=Email('test@test.fr'),
        telephone=Telephone('0645789845'), company_name="company_test",
        commercial_contact=user_commercial.id
    )

def test_client_create(client):

    assert type(client.id) == int
    assert type(client.fullname) == str
    assert type(client.email) == Email
    assert type(client.telephone) == Telephone
    assert type(client.company_name) == str
    assert type(client.commercial_contact) == int
    assert type(client.created_at) == datetime
    assert type(client.updated_at) == datetime

def test_client_update_info(client):
    fullname = "futur test"
    email = Email('futur@test.fr')
    telephone = Telephone('0999999999')
    company_name = "futur_test"
    client.update_info(fullname=fullname, email=email, telephone=telephone, company_name=company_name)

    assert client.fullname == fullname
    assert client.email == email
    assert client.telephone == telephone
    assert client.company_name == company_name
    assert client.updated_at != client.created_at

def test_client_can_by_update(client, user_commercial):
    user = User(id=2, full_name="test2", email=Email("test2@test.fr"),
                password="dfsdfsf", role=Role.COMMERCIAL,)

    assert client.can_be_updated_by(user) is False
    assert client.can_be_updated_by(user_commercial) is True
