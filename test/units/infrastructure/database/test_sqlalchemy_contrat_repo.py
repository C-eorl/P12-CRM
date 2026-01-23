from typing import List

from sqlalchemy import select

from src.domain.entities.entities import Contrat
from src.domain.entities.value_objects import Money
from src.infrastructures.database.models import ContratModel


def test_save_contrat_create(contrat_SQLAlchemy_repository, contrat, session):
    init_count_contrat = session.query(ContratModel).count()
    saved_contrat = contrat_SQLAlchemy_repository.save(contrat)
    current_count_contrat = session.query(ContratModel).count()
    assert isinstance(saved_contrat, Contrat)
    assert init_count_contrat + 1 == current_count_contrat

def test_save_user_update(contrat_SQLAlchemy_repository):
    """test save method for update client"""
    saved_contrat = contrat_SQLAlchemy_repository.find_by_id(4)

    saved_contrat.contrat_amount = Money(500)
    contrat_SQLAlchemy_repository.save(saved_contrat)

    updated_contrat = contrat_SQLAlchemy_repository.find_by_id(4)
    assert updated_contrat.contrat_amount == Money(500)

def test_find_by_id(contrat_SQLAlchemy_repository):
    """test find by id method """
    contrat_find = contrat_SQLAlchemy_repository.find_by_id(3)

    assert isinstance(contrat_find, Contrat)
    assert contrat_find.client_id == 3
    assert contrat_find.commercial_contact_id == 3


def test_find_by_invalid_id(contrat_SQLAlchemy_repository):
    """test find all method """
    find_contrat = contrat_SQLAlchemy_repository.find_by_id(45)

    assert find_contrat is None

def test_find_all(contrat_SQLAlchemy_repository, session):
    """test find all method """
    all_contrats = contrat_SQLAlchemy_repository.find_all()

    assert isinstance(all_contrats, List)
    actual_count_contrat = session.query(ContratModel).count()
    assert len(all_contrats) == actual_count_contrat

def test_find_by_commercial_contact(contrat_SQLAlchemy_repository, session):
    """test find all method """
    all_contrats = contrat_SQLAlchemy_repository.find_by_commercial_contact(3)

    assert isinstance(all_contrats, List)
    actual_count_contrat = session.query(ContratModel).where(ContratModel.commercial_contact_id == 3).count()
    assert len(all_contrats) == actual_count_contrat

def test_find_by_client_id(contrat_SQLAlchemy_repository, session):
    """test find all method """
    all_contrats = contrat_SQLAlchemy_repository.find_by_client_id(1)

    assert isinstance(all_contrats, List)
    actual_count_contrat = session.query(ContratModel).where(ContratModel.client_id == 1).count()
    assert len(all_contrats) == actual_count_contrat

def test_delete(contrat_SQLAlchemy_repository, session, contrat):
    """test delete method """
    init_count_contrat = session.query(ContratModel).count()
    contrat_SQLAlchemy_repository.save(contrat)
    session.commit()
    last_contrat = session.execute(select(ContratModel)).scalars().all()[-1]
    delete_contrat = contrat_SQLAlchemy_repository.delete(last_contrat.id)

    assert delete_contrat is None
    actual_count_contrat = session.query(ContratModel).count()
    assert actual_count_contrat == init_count_contrat