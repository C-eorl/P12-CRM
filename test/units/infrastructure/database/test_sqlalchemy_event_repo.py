from typing import List

from sqlalchemy import select

from src.domain.entities.entities import Event
from src.infrastructures.database.models import EventModel



def test_save_event_create(event_SQLAlchemy_repository, event, session):
    init_count_event = session.query(EventModel).count()
    saved_event = event_SQLAlchemy_repository.save(event)
    current_count_event = session.query(EventModel).count()
    assert isinstance(saved_event, Event)
    assert init_count_event + 1 == current_count_event

def test_save_event_update(event_SQLAlchemy_repository):
    """test save method for update client"""
    saved_event = event_SQLAlchemy_repository.find_by_id(5)

    saved_event.attendees = 500
    event_SQLAlchemy_repository.save(saved_event)

    updated_event = event_SQLAlchemy_repository.find_by_id(5)
    assert updated_event.attendees == 500

def test_find_by_id(event_SQLAlchemy_repository):
    """test find by id method """
    event_find = event_SQLAlchemy_repository.find_by_id(5)

    assert isinstance(event_find, Event)
    assert event_find.client_id == 1
    assert event_find.support_contact_id == 5
    assert event_find.location == "2 rue des test, Nantes"


def test_find_by_invalid_id(event_SQLAlchemy_repository):
    """test find all method """
    find_event = event_SQLAlchemy_repository.find_by_id(455)

    assert find_event is None

def test_find_all(event_SQLAlchemy_repository, session):
    """test find all method """
    all_events = event_SQLAlchemy_repository.find_all()

    assert isinstance(all_events, List)
    actual_count_events = session.query(EventModel).count()
    assert len(all_events) == actual_count_events

def test_find_by_contrat_id(event_SQLAlchemy_repository, session):
    """test find all method """
    all_events = event_SQLAlchemy_repository.find_by_contrat_id(2)

    assert isinstance(all_events, List)
    actual_count_event = session.query(EventModel).where(EventModel.contrat_id == 2).count()
    assert len(all_events) == actual_count_event

def test_find_by_support_contact_id(event_SQLAlchemy_repository, session):
    """test find all method """
    all_events = event_SQLAlchemy_repository.find_by_support_contact_id(6)

    assert isinstance(all_events, List)
    actual_count_event = session.query(EventModel).where(EventModel.support_contact_id == 6).count()
    assert len(all_events) == actual_count_event

def test_find_by_client_id(event_SQLAlchemy_repository, session):
    """test find all method """
    all_events = event_SQLAlchemy_repository.find_by_client_id(1)

    assert isinstance(all_events, List)
    actual_count_event = session.query(EventModel).where(EventModel.client_id == 1).count()
    assert len(all_events) == actual_count_event

def test_delete(event_SQLAlchemy_repository, session, event):
    """test delete method """
    init_count_event = session.query(EventModel).count()
    event_SQLAlchemy_repository.save(event)
    session.commit()
    last_event = session.execute(select(EventModel)).scalars().all()[-1]
    delete_event = event_SQLAlchemy_repository.delete(last_event.id)

    assert delete_event is None
    actual_count_event = session.query(EventModel).count()
    assert actual_count_event == init_count_event