from datetime import datetime

from src.domain.entities.entities import Event
from src.domain.entities.enums import Role
from src.domain.policies.user_policy import RequestPolicy
from src.use_cases.event_use_cases import CreateEventUseCase, CreateEventRequest, CreateEventResponse, \
    UpdateEventUseCase, UpdateEventRequest, UpdateEventResponse, GetEventUseCase, GetEventRequest, GetEventResponse, \
    DeleteEventUseCase, DeleteEventRequest, DeleteEventResponse, ListEventRequest, ListEventUseCase, ListEventResponse, \
    AssignSupportEventUseCase, AssignSupportEventRequest, AssignSupportEventResponse


######################################################################
#                            Create Contrat Use Case                 #
######################################################################
def test_create_event(event_repository):
    """Test creating a new contrat via use case"""
    repo = event_repository
    uc = CreateEventUseCase(repo)

    request = CreateEventRequest(
        name = "ttes",
        contrat_id= 80,
        client_id= 3,
        start_date= datetime.strptime("2026-05-10 10:00:00", "%Y-%m-%d %H:%M:%S"),
        end_date= datetime.strptime("2026-05-10 18:00:00", "%Y-%m-%d %H:%M:%S"),
        location="rtret",
        attendees=450,
        notes="",
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.COMMERCIAL},
            ressource="EVENT",
            action="create",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, CreateEventResponse)
    assert response.success is True
    assert isinstance(response.event, Event)

    found = repo.find_by_id(response.event.id)
    assert found is not None

def test_create_event_no_commercial_user(event_repository):
    """Test creating a contrat without gestion permission"""
    repo = event_repository
    uc = CreateEventUseCase(repo)

    request = CreateEventRequest(
        name="ttes",
        contrat_id=80,
        client_id=3,
        start_date=datetime.strptime("2026-05-10 10:00:00", "%Y-%m-%d %H:%M:%S"),
        end_date=datetime.strptime("2026-05-10 18:00:00", "%Y-%m-%d %H:%M:%S"),
        location="rtret",
        attendees=450,
        notes="",
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="EVENT",
            action="create",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, CreateEventResponse)
    assert response.success is False
    assert response.event is None

######################################################################
#                            Update Contrat Use Case                 #
######################################################################
def test_update_event(event_repository):
    """Test updating a contrat via use case"""
    repo = event_repository
    uc = UpdateEventUseCase(repo)

    request = UpdateEventRequest(
        event_id=1,
        name="update event",
        start_date=None,
        end_date=None,
        location=None,
        attendees=None,
        notes=None,
        authorization=RequestPolicy(
            user={"user_current_id": 60, "user_current_role": Role.SUPPORT},
            ressource="EVENT",
            action="update",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, UpdateEventResponse)
    assert response.success is True

    updated = repo.find_by_id(1)
    assert updated.name == "update event"

def test_update_contrat_not_found(event_repository):
    """Test updating a non-existing contrat"""
    repo = event_repository
    uc = UpdateEventUseCase(repo)

    request = UpdateEventRequest(
        event_id=1150,
        name="update event",
        start_date=None,
        end_date=None,
        location=None,
        attendees=None,
        notes=None,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.SUPPORT},
            ressource="EVENT",
            action="update",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, UpdateEventResponse)
    assert response.success is False

def test_update_event_no_permission(event_repository):
    """Test updating a contrat without permission"""
    repo = event_repository
    uc = UpdateEventUseCase(repo)

    request = UpdateEventRequest(
        event_id=1,
        name="update event",
        start_date=None,
        end_date=None,
        location=None,
        attendees=None,
        notes=None,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="EVENT",
            action="update",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, UpdateEventResponse)
    assert response.success is False

######################################################################
#                            List Contrat Use Case                   #
######################################################################
def test_list_event(event_repository):
    """Test listing contrats"""
    request = ListEventRequest(
        support_contact_id=3,
        list_filter=None
    )

    repo = event_repository
    uc = ListEventUseCase(repo)

    response = uc.execute(request)

    assert isinstance(response, ListEventResponse)
    assert response.success is True
    assert isinstance(response.events, list)

######################################################################
#                            Get Contrat Use Case                   #
######################################################################
def test_get_event_by_id(event_repository):
    """Test get contrat by id"""
    repo = event_repository
    uc = GetEventUseCase(repo)

    request = GetEventRequest(event_id=1)
    response = uc.execute(request)

    assert isinstance(response, GetEventResponse)
    assert response.success is True
    assert isinstance(response.event, Event)

def test_get_event_invalid_id(event_repository):
    """Test get contrat with invalid id"""
    repo = event_repository
    uc = GetEventUseCase(repo)

    request = GetEventRequest(event_id=1450)
    response = uc.execute(request)


    assert isinstance(response, GetEventResponse)
    assert response.success is False

######################################################################
#                            Delete Contrat Use Case                 #
######################################################################
def test_delete_event_admin(event_repository):
    """Test deleting a contrat as admin"""
    repo = event_repository
    uc = DeleteEventUseCase(repo)

    request = DeleteEventRequest(
        event_id=1,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.ADMIN},
            ressource="EVENT",
            action="delete",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, DeleteEventResponse)
    assert response.success is True
    assert repo.find_by_id(1) is None

def test_delete_event_no_admin(event_repository):
    """Test deleting a contrat without admin role"""
    repo = event_repository
    uc = DeleteEventUseCase(repo)

    request = DeleteEventRequest(
        event_id=1,
        authorization=RequestPolicy(
            user={"user_current_id": 2, "user_current_role": Role.GESTION},
            ressource="EVENT",
            action="delete",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, DeleteEventResponse)
    assert response.success is False

def test_assign_event(event_repository, user_repository):
    """Test assigning a support user to event"""
    repo = event_repository
    user_repo = user_repository
    uc = AssignSupportEventUseCase(repo, user_repo)
    request = AssignSupportEventRequest(
        event_id=2,
        support_user_id=2,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="EVENT",
            action="assign",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, AssignSupportEventResponse)
    assert response.success is True


def test_assign_no_event(event_repository, user_repository):
    """Test assigning a support user to event"""
    repo = event_repository
    user_repo = user_repository
    uc = AssignSupportEventUseCase(repo, user_repo)
    request = AssignSupportEventRequest(
        event_id=456,
        support_user_id=2,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="EVENT",
            action="assign",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, AssignSupportEventResponse)
    assert response.success is False


def test_assign_event_no_support_user(event_repository, user_repository):
    """Test assigning a support user to event"""
    repo = event_repository
    user_repo = user_repository
    uc = AssignSupportEventUseCase(repo, user_repo)
    request = AssignSupportEventRequest(
        event_id=2,
        support_user_id=1,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="EVENT",
            action="assign",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, AssignSupportEventResponse)
    assert response.success is False