##############################################################################
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List

from src.domain.entities.entities import Event
from src.domain.interfaces.repository import EventRepository, UserRepository, ContratRepository, ClientRepository
from src.domain.policies.user_policy import UserPolicy, RequestPolicy


@dataclass
class CreateEventRequest:
    name: str
    contrat_id: int
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
    msg: Optional[str] = None


class CreateEventUseCase:
    """Use case for creating a new contrat"""

    def __init__(
            self, event_repository: EventRepository,
            contrat_repository: ContratRepository,
            client_repository: ClientRepository
    ):
        self.event_repository = event_repository
        self.contrat_repository = contrat_repository
        self.client_repository = client_repository

    def execute(self, request: CreateEventRequest) -> CreateEventResponse:

        policy = UserPolicy(request.authorization)
        if not policy.is_allowed():
            return CreateEventResponse(
                success=False,
                error="Permission",
                msg="Seuls les membres commerciaux peuvent créer des évènements"
            )
        # validation contrat existe
        if not self.contrat_repository.exist(request.contrat_id):
            return CreateEventResponse(
                success=False,
                error="Ressource",
                msg=f"le Contrat #{request.contrat_id} n'existe pas"
            )

        contrat = self.contrat_repository.find_by_id(request.contrat_id)
        # Validation si contrat associé commercial
        if contrat.commercial_contact_id != request.authorization.user["user_current_id"]:
            return CreateEventResponse(
                success=False,
                error="Permission",
                msg=f"le Contrat #{request.contrat_id} n'est pas associé à vous"
            )

        if not contrat.has_sign():
            return CreateEventResponse(
                success=False,
                error="Erreur Métier",
                msg=f"Contrat {request.contrat_id} n'est pas signé"
            )
        # Validation valeur
        if request.start_date < datetime.now():
            return CreateEventResponse(
                success=False,
                error="Erreur Métier",
                msg="La date de début est déjà passé"
            )
        if request.end_date <= request.start_date:
            return CreateEventResponse(
                success=False,
                error="Erreur Métier",
                msg="La date de fin doit être après la date de début"
            )
        if request.attendees <= 0:
            return CreateEventResponse(
                success=False,
                error="Erreur Métier",
                msg="Le nombre de participants doit être positif"
            )

        client_id = contrat.client_id

        event = Event(
            id=  None,
            name =  request.name,
            contrat_id = request.contrat_id,
            client_id = client_id,
            support_contact_id = None,
            start_date = request.start_date,
            end_date = request.end_date,
            location = request.location,
            attendees = request.attendees,
            notes = request.notes,
            )

        saved_event = self.event_repository.save(event)
        return CreateEventResponse(success=True, event=saved_event)

##############################################################################
@dataclass
class UpdateEventRequest:
    event_id: int
    name: Optional[str]
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
    msg: Optional[str] = None


class UpdateEventUseCase:
    """Use case for updating a contrat"""

    def __init__(self, event_repository: EventRepository):
        self.repository = event_repository

    def execute(self, request: UpdateEventRequest) -> UpdateEventResponse:

        event = self.repository.find_by_id(request.event_id)
        if not event:
            return UpdateEventResponse(
                success=False,
                error="Ressource",
                msg="Événement non trouvé"
            )

        policy = UserPolicy(request.authorization)
        request.authorization.context = event
        if not policy.is_allowed():
            return UpdateEventResponse(
                success=False,
                error="Permission",
                msg="Seuls les membres support peuvent créer des évènements"
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
class EventFilter(Enum):
    WITHOUT_SUPPORT = "no-support"
    MINE = "mine"

@dataclass
class ListEventRequest:
    support_contact_id: int
    list_filter: Optional[EventFilter]

@dataclass
class ListEventResponse:
    success: bool
    events: List[Event] = None
    error: Optional[str] = None
    msg: Optional[str] = None

class ListEventUseCase:
    """Use case for listing contrats"""

    def __init__(self, event_repository: EventRepository):
        self.repository = event_repository

    def execute(self, request: ListEventRequest) -> ListEventResponse:
        criteres = dict()
        match request.list_filter:
            case EventFilter.MINE:
                criteres["support_contact_id"] = request.support_contact_id
            case EventFilter.WITHOUT_SUPPORT:
                criteres["support_contact"] = False

        events = self.repository.find_all(criteres)
        if not events:
            return ListEventResponse(
                success=False,
                error="Ressource",
                msg="Aucun évènement trouvé"
            )

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
    msg: Optional[str] = None


class GetEventUseCase:
    """Use case for retrieving a contrat"""

    def __init__(self, event_repository: EventRepository):
        self.repository = event_repository

    def execute(self, request: GetEventRequest) -> GetEventResponse:

        event = self.repository.find_by_id(request.event_id)
        if not event:
            return GetEventResponse(
                success=False,
                error="Ressource",
                msg="Evenement non trouvé"
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
    msg: Optional[str] = None


class DeleteEventUseCase:
    """Use case for deleting a contrat"""

    def __init__(self, event_repository: EventRepository):
        self.repository = event_repository

    def execute(self, request: DeleteEventRequest) -> DeleteEventResponse:

        event = self.repository.find_by_id(request.event_id)
        if not event:
            return DeleteEventResponse(
                success=False,
                error="Ressource",
                msg="Evenement non trouvé"
            )

        policy = UserPolicy(request.authorization)
        if not policy.is_allowed():
            return DeleteEventResponse(
                success=False,
                error="Permission",
                msg="Seuls les membres administrateur peuvent supprimer des évènements"
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
    msg: Optional[str] = None

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
                error="Permission",
                msg="Seuls les membres support peuvent créer des évènements"
            )

        event = self.repository.find_by_id(request.event_id)
        if not event:
            return AssignSupportEventResponse(
                success=False,
                error="Ressource",
                msg="Evenement non trouvé"
            )

        if event.has_support_contact():
            return AssignSupportEventResponse(
                success=False,
                error="Erreur Métier",
                msg="L'évènement a déjà un contact support"
            )

        user = self.user_repository.find_by_id(request.support_user_id)
        if not user:
            return AssignSupportEventResponse(
                success=False,
                error="Ressource",
                msg="Utilisateur non trouvé"
            )
        try:
            event.assign_support(user)
        except PermissionError as e:
            return AssignSupportEventResponse(
                success=False,
                error="Permission",
                msg=str(e)
            )

        self.repository.save(event)
        return AssignSupportEventResponse(success=True)