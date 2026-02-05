from datetime import datetime

import pytest

from src.domain.entities.entities import Event
from src.domain.entities.exceptions import BusinessRuleViolation


def test_create_valid_event(event):

    assert isinstance(event, Event)


def test_assign_support(event, user_support):
    """Assign user support (id: 2) to event"""
    user_support.id = 2
    event.assign_support(user_support)
    assert event.support_contact_id == 2

def test_assign_not_support(event, user_commercial, user_gestion):
    """Assign not user support to event"""
    users = [user_commercial, user_gestion]

    for user in users:
        with pytest.raises(PermissionError):
            event.assign_support(user)

def test_has_support(event):
    """Check if support is assigned to event"""
    assert event.has_support_contact() == True

def test_has_not_support():
    """Check if not support is assigned to event"""
    event = Event(
        id=1,
        name="test event",
        contrat_id=1,
        client_id=1,
        support_contact_id=None,
        start_date=datetime(2026, 5, 15),
        end_date=datetime(2026, 5, 20),
        location="2 rue des test, Nantes",
        attendees=15,
        notes=""
    )
    assert event.has_support_contact() == False

def test_can_be_updated_by_gestion(event, user_gestion):
    """Check if gestion user can update event"""
    assert event.can_be_updated_by(user_gestion) == True

def test_can_be_updated_by_support(event, user_support):
    """Check if support_user assigned can update event"""
    user_support.id = 5
    assert event.can_be_updated_by(user_support) == True

def test_can_be_updated_by_not_assigned_support(event, user_support2):
    """Check if support_user assigned can update event"""
    assert event.can_be_updated_by(user_support2) == False

def test_can_be_updated_by_commercial(event, user_commercial):
    """Check if support_user assigned can update event"""
    assert event.can_be_updated_by(user_commercial) == False

def test_update_info_valid(event):
    """Verifies the change with valid data"""
    event.update_info(
        name= "test modify",
        location = "2 avenue modifié",
        attendees = 1000,
        notes = "lorem ipsum",
        start_date = datetime(2026, 5, 15, 9, 45),
        end_date = datetime(2026, 5, 20, 20, 00)
    )

    assert event.name == "test modify"
    assert event.location == "2 avenue modifié"
    assert event.attendees == 1000
    assert event.notes == "lorem ipsum"
    assert event.updated_at != event.created_at

def test_update_info_invalid(event):
    """Verifies the change with valid data"""
    with pytest.raises(BusinessRuleViolation):
        event.update_info(
            name=12, # int attend str
            location="2 avenue modifié",
            attendees=1000,
            notes="lorem ipsum",
            start_date= None,
            end_date= None
        )

    with pytest.raises(BusinessRuleViolation):
        event.update_info(
            name="",
            location="",
            attendees=0,
            notes=0,
            start_date="dsd",
            end_date="dsdd"
        )