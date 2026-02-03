##############################################################################
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from src.domain.entities.entities import User, Event
from src.domain.entities.enums import ContractStatus
from src.domain.entities.value_objects import Money
from src.domain.interfaces.repository import EventRepository, UserRepository
from src.domain.policies.user_policy import UserPolicy, RequestPolicy


@dataclass
class CreateEventRequest:
    name: str
    contrat_id: int
    client_id: int
    support_contact_id: Optional[int]
    start_date: datetime
    end_date: datetime
    location: str
    attendees: int
    notes: str
    authorization: RequestPolicy


@dataclass
class CreateEventResponse:
    success: bool
    event: Optional[Event] = None
    error: Optional[str] = None


class CreateEventUseCase:
    """Use case for creating a new contrat"""

    def __init__(self, event_repository: EventRepository):
        self.repository = event_repository

    def execute(self, request: CreateEventRequest) -> CreateEventResponse:

        policy = UserPolicy(request.authorization)
        if not policy.is_allowed():
            return CreateEventResponse(
                success=False,
                error="Seuls les membres support peuvent créer des évènements"
            )

        event = Event(
            id=  None,
            name =  request.name,
            contrat_id = request.contrat_id,
            client_id = request.client_id,
            support_contact_id = request.support_contact_id,
            start_date = request.start_date,
            end_date = request.end_date,
            location = request.location,
            attendees = request.attendees,
            notes = request.notes,
            )

        saved_event = self.repository.save(event)
        return CreateEventResponse(success=True, event=saved_event)

##############################################################################
@dataclass
class UpdateEventRequest:
    event_id: int
    name: Optional[str]
    # contrat id
    # client id
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    location: Optional[str]
    attendees: Optional[int]
    notes: Optional[str]
    authorization: RequestPolicy


@dataclass
class UpdateEventResponse:
    success: bool
    event: Optional[Event] = None
    error: Optional[str] = None


class UpdateEventUseCase:
    """Use case for updating a contrat"""

    def __init__(self, event_repository: EventRepository):
        self.repository = event_repository

    def execute(self, request: UpdateEventRequest) -> UpdateEventResponse:

        event = self.repository.find_by_id(request.event_id)
        if not event:
            return UpdateEventResponse(
                success=False,
                error="Événement non trouvé"
            )

        policy = UserPolicy(request.authorization)
        request.authorization.context = event
        if not policy.is_allowed():
            return UpdateEventResponse(
                success=False,
                error="Seuls les membres support peuvent créer des évènements"
            )

        event.update_info(
            request.name,
            request.start_date,
            request.end_date,
            request.location,
            request.attendees,
            request.notes,
        )


        updated_event = self.repository.save(event)
        return UpdateEventResponse(success=True, event=updated_event)

##############################################################################
@dataclass
class ListEventResponse:
    success: bool
    events: List[Event] = None
    error: Optional[str] = None


class ListEventUseCase:
    """Use case for listing contrats"""

    def __init__(self, event_repository: EventRepository):
        self.repository = event_repository

    def execute(self) -> ListEventResponse:
        events = self.repository.find_all()
        return ListEventResponse(success=True, events=events)

##############################################################################
@dataclass
class GetEventRequest:
    event_id: int


@dataclass
class GetEventResponse:
    success: bool
    event: Optional[Event] = None
    error: Optional[str] = None


class GetEventUseCase:
    """Use case for retrieving a contrat"""

    def __init__(self, event_repository: EventRepository):
        self.repository = event_repository

    def execute(self, request: GetEventRequest) -> GetEventResponse:

        event = self.repository.find_by_id(request.event_id)
        if not event:
            return GetEventResponse(
                success=False,
                error="Evenement non trouvé"
            )

        return GetEventResponse(success=True, event=event)

##############################################################################
@dataclass
class DeleteEventRequest:
    event_id: int
    authorization: RequestPolicy


@dataclass
class DeleteEventResponse:
    success: bool
    error: Optional[str] = None


class DeleteEventUseCase:
    """Use case for deleting a contrat"""

    def __init__(self, event_repository: EventRepository):
        self.repository = event_repository

    def execute(self, request: DeleteEventRequest) -> DeleteEventResponse:

        event = self.repository.find_by_id(request.event_id)
        if not event:
            return DeleteEventResponse(
                success=False,
                error="Evenement non trouvé"
            )

        policy = UserPolicy(request.authorization)
        if not policy.is_allowed():
            return DeleteEventResponse(
                success=False,
                error="Seuls les membres administrateur peuvent créer des évènements"
            )

        self.repository.delete(event.id)
        return DeleteEventResponse(success=True)

##############################################################################

@dataclass
class AssignSupportEventRequest:
    event_id: int
    support_user_id: int
    authorization: RequestPolicy

@dataclass
class AssignSupportEventResponse:
    success: bool
    error: Optional[str] = None

class AssignSupportEventUseCase:
    """Use case for assigning support events"""
    def __init__(self, event_repository: EventRepository, user_repository: UserRepository):
        self.repository = event_repository
        self.user_repository = user_repository

    def execute(self, request: AssignSupportEventRequest) -> AssignSupportEventResponse:

        policy = UserPolicy(request.authorization)
        if not policy.is_allowed():
            return AssignSupportEventResponse(
                success=False,
                error="Seuls les membres support peuvent créer des évènements"
            )

        event = self.repository.find_by_id(request.event_id)
        if not event:
            return AssignSupportEventResponse(
                success=False,
                error="Evenement non trouvé"
            )

        if event.has_support_contact():
            return AssignSupportEventResponse(
                success=False,
                error="L'évènement a déjà un contact support"
            )

        user = self.user_repository.find_by_id(request.support_user_id)
        if not user:
            return AssignSupportEventResponse(
                success=False,
                error="Utilisateur support non trouvé"
            )
        try:
            event.assign_support(user)
        except PermissionError as e:
            return AssignSupportEventResponse(
                success=False,
                error=str(e)
            )

        return AssignSupportEventResponse(success=True)