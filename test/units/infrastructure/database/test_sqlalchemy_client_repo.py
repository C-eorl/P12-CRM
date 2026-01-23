from typing import List

from sqlalchemy import select

from src.domain.entities.entities import Client
from src.infrastructures.database.models import ClientModel


def test_save_client_create(client_SQLAlchemy_repository, client):
    """test save method for create client"""
    saved_client = client_SQLAlchemy_repository.save(client)

    assert saved_client.id is not None
    assert saved_client.fullname == client.fullname
    assert saved_client.email.address == client.email.address


def test_save_client_update(client_SQLAlchemy_repository, client):
    """test save method for update client"""
    saved_client = client_SQLAlchemy_repository.find_by_id(6)

    saved_client.fullname = "SQL test"
    updated_client = client_SQLAlchemy_repository.save(saved_client)

    assert updated_client.fullname == "SQL test"
    assert updated_client.id == saved_client.id

def test_find_by_id(client_SQLAlchemy_repository):
    """test find by id method """
    find_client = client_SQLAlchemy_repository.find_by_id(6)

    assert isinstance(find_client, Client)
    assert find_client.email.address == "test@test.fr"

def test_find_by_invalid_id(client_SQLAlchemy_repository):
    """test find all method """
    find_client = client_SQLAlchemy_repository.find_by_id(45)

    assert find_client is None

def test_find_all(client_SQLAlchemy_repository, session):
    """test find all method """
    all_clients = client_SQLAlchemy_repository.find_all()

    assert isinstance(all_clients, List)
    actual_count_client = session.query(ClientModel).count()
    assert len(all_clients) == actual_count_client

def test_delete(client_SQLAlchemy_repository, session, client):
    """test delete method """
    init_count_client = session.query(ClientModel).count()
    client_SQLAlchemy_repository.save(client)
    session.commit()
    last_client = session.execute(select(ClientModel)).scalars().all()[-1]
    delete_client = client_SQLAlchemy_repository.delete(last_client.id)


    assert delete_client is None
    actual_count_client = session.query(ClientModel).count()
    assert actual_count_client == init_count_client