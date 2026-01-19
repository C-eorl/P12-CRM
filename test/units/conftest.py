from datetime import datetime

import pytest

from src.domain.entities.entities import User, Client, Contrat, Event
from src.domain.entities.enums import Role, ContractStatus
from src.domain.entities.value_objects import Email, Telephone, Money
from src.infrastructures.repositories.fake_client_repository import FakeClientRepository


@pytest.fixture(scope="module")
def user_commercial():
    return User(id=1, full_name="test test",
                email=Email("test@test.com"), password="sfsefs",
                role=Role.COMMERCIAL)

@pytest.fixture
def user_support():
    return User(id=2, full_name="test test",
                email=Email("test@test.com"), password="sfsefs",
                role=Role.SUPPORT)

@pytest.fixture
def user_gestion():
    return User(id=3, full_name="test test",
                email=Email("test@test.com"), password="sfsefs",
                role=Role.GESTION)

@pytest.fixture
def user_commercial2():
    return User(id=2, full_name="test2", email=Email("test2@test.fr"),
                password="dfsdfsf", role=Role.COMMERCIAL,)

@pytest.fixture
def user_support2():
    return User(id=45, full_name="test test",
                email=Email("test@test.com"), password="sfsefs",
                role=Role.SUPPORT)

@pytest.fixture
def client(user_commercial):
    return Client(
        id=None,fullname="test test", email=Email('test@test.fr'),
        telephone=Telephone('0645789845'), company_name="company_test",
        commercial_contact_id=user_commercial.id
    )

@pytest.fixture
def client2(user_commercial):
    return Client(
        id=None,fullname="test double", email=Email('test42@test.fr'),
        telephone=Telephone('0645789845'), company_name="company_test2",
        commercial_contact_id=user_commercial.id
    )

@pytest.fixture(scope="function")
def contrat():
    return Contrat(
        id=1,
        client= 5,
        commercial_contact_id= 1,
        contrat_amount=Money(100),
        balance_due=Money(100),
        status= ContractStatus.UNSIGNED
    )

@pytest.fixture
def event():
    return Event(
        id=1,
        name="test event",
        contrat_id= 1,
        client_id= 1,
        support_contact_id= 2,
        start_date= datetime(2026, 5,15),
        end_date= datetime(2026, 5,20),
        location="2 rue des test, Nantes",
        attendees= 150,
        notes=""
    )

@pytest.fixture
def client_repository(client, client2):
    repo = FakeClientRepository()
    repo.save(client)
    repo.save(client2)
    return repo