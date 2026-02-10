import os
from datetime import datetime
from email._policybase import Policy

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.entities.entities import User, Client, Contrat, Event
from src.domain.entities.enums import Role, ContractStatus
from src.domain.entities.value_objects import Email, Telephone, Money
from src.domain.policies.user_policy import UserPolicy, RequestPolicy
from src.infrastructures.database.models import Base
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyClientRepository, SQLAlchemyUserRepository, \
    SQLAlchemyContratRepository, SQLAlchemyEventRepository
from src.infrastructures.repositories.fake_client_repository import FakeClientRepository, FakeUserRepository, \
    FakeContratRepository, FakeEventRepository

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

@pytest.fixture
def user_commercial():
    return User(id=None, fullname="test test",
                email=Email("test@test.com"), password="sfsefs",
                role=Role.COMMERCIAL)

@pytest.fixture
def user_support():
    return User(id=None, fullname="test test",
                email=Email("test@test.com"), password="sfsefs",
                role=Role.SUPPORT)

@pytest.fixture
def user_gestion():
    return User(id=None, fullname="test test",
                email=Email("test@test.com"), password="sfsefs",
                role=Role.GESTION)

@pytest.fixture
def user_commercial2():
    return User(id=None, fullname="test2", email=Email("test2@test.fr"),
                password="dfsdfsf", role=Role.COMMERCIAL,)

@pytest.fixture
def user_support2():
    return User(id=None, fullname="test test",
                email=Email("test@test.com"), password="sfsefs",
                role=Role.SUPPORT)

@pytest.fixture
def client(user_commercial):
    return Client(
        id=None,fullname="test test", email=Email('test@test.fr'),
        telephone=Telephone('0645789845'), company_name="company_test",
        commercial_contact_id=3
    )

@pytest.fixture
def client2(user_commercial):
    return Client(
        id=None,fullname="test double", email=Email('test42@test.fr'),
        telephone=Telephone('0645789845'), company_name="company_test2",
        commercial_contact_id=3
    )

@pytest.fixture(scope="function")
def contrat():
    return Contrat(
        id=None,
        client_id= 3,
        commercial_contact_id= 4,
        contrat_amount=Money(100),
        balance_due=Money(100),
        status= ContractStatus.UNSIGNED
    )

@pytest.fixture
def contrat2():
    return Contrat(
        id=None,
        client_id= 6,
        commercial_contact_id= 5,
        contrat_amount=Money(100),
        balance_due=Money(100),
        status= ContractStatus.UNSIGNED
    )

@pytest.fixture
def event():
    return Event(
        id=None,
        name="test event",
        contrat_id= 4,
        client_id= 3,
        support_contact_id= 60,
        start_date= datetime(2026, 5,15),
        end_date= datetime(2026, 5,20),
        location="2 rue des test, Nantes",
        attendees= 150,
        notes=""
        )


@pytest.fixture
def event2():
    return Event(
        id=None,
        name="test event2",
        contrat_id= 4,
        client_id= 3,
        support_contact_id= None,
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

@pytest.fixture
def user_repository(user_commercial, user_support, user_gestion):
    repo = FakeUserRepository()
    repo.save(user_commercial)
    repo.save(user_support)
    repo.save(user_gestion)
    return repo

@pytest.fixture
def contrat_repository(contrat, contrat2):
    repo = FakeContratRepository()
    repo.save(contrat)
    repo.save(contrat2)
    return repo

@pytest.fixture
def event_repository(event,event2, client):
    repo = FakeEventRepository()
    repo.save(event)
    repo.save(event2)
    return repo

@pytest.fixture(scope="function")
def session():
    engine = create_engine(DATABASE_URL, echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    trans = session.begin()

    yield session

    session.rollback()
    session.close()

@pytest.fixture
def policy(request):
    return UserPolicy(request)

@pytest.fixture
def client_SQLAlchemy_repository(session):
    return SQLAlchemyClientRepository(session)

@pytest.fixture
def user_SQLAlchemy_repository(session):
    return SQLAlchemyUserRepository(session)

@pytest.fixture
def contrat_SQLAlchemy_repository(session):
    return SQLAlchemyContratRepository(session)

@pytest.fixture
def event_SQLAlchemy_repository(session):
    return SQLAlchemyEventRepository(session)