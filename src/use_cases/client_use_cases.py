from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


from src.domain.entities.entities import Client
from src.domain.entities.exceptions import ValidationError, InvalidEmailError, InvalidPhoneError
from src.domain.entities.value_objects import Email, Telephone

from src.domain.interfaces.repository import ClientRepository
from src.domain.policies.user_policy import UserPolicy, RequestPolicy


################################################################################################
@dataclass
class CreateClientRequest:
    """Request to create a new client"""
    fullname: str
    email: str
    telephone: str
    company_name: str
    authorization: RequestPolicy


@dataclass
class CreateClientResponse:
    """Response to create a new client"""
    success: bool
    client: Optional[Client] = None
    error: Optional[str] = None
    msg: Optional[str] = None


class CreateClientUseCase:
    """Use case for creating a new client"""

    def __init__(self, client_repository: ClientRepository):
        self.repository = client_repository

    def execute(self, request: CreateClientRequest) -> CreateClientResponse:

        policy = UserPolicy(request.authorization)

        if not policy.is_allowed():
            return CreateClientResponse(
                success=False,
                error="Permission",
                msg="Seuls les membres commerciaux peuvent créer des clients"
            )

        try:
            email = Email(request.email)
            telephone = Telephone(request.telephone)
        except (ValidationError, InvalidEmailError, InvalidPhoneError) as e:
            return CreateClientResponse(
                success=False,
                error=str(e),
                msg="Email ou Telephone n'est pas valide"
            )

        client = Client(
            id = None,
            fullname=request.fullname,
            email = email,
            telephone = telephone,
            company_name=request.company_name,
            commercial_contact_id=request.authorization.user["user_current_id"])

        saved_client = self.repository.save(client)

        return CreateClientResponse(success=True, client=saved_client)

################################################################################################
@dataclass
class UpdateClientRequest:
    client_id: int
    fullname: Optional[str]
    email: Optional[str]
    telephone: Optional[str]
    company_name: Optional[str]
    authorization: RequestPolicy


@dataclass
class UpdateClientResponse:
    success: bool
    client: Optional[Client] = None
    error: Optional[str] = None
    msg: Optional[str] = None


class UpdateClientUseCase:
    """
    Use case for updating associated client.
    """
    def __init__(self, client_repository: ClientRepository):
        self.repository = client_repository

    def execute(self, request: UpdateClientRequest):
        # Permission liée au role

        client = self.repository.find_by_id(request.client_id)
        if not client:
            return UpdateClientResponse(
                success=False,
                error="Ressource",
                msg=f"Client non trouvé"
            )

        policy = UserPolicy(request.authorization)
        request.authorization.context = client
        if not policy.is_allowed():
            return UpdateClientResponse(
                success=False,
                error="Permission",
                msg="Seuls les membres commerciaux associé au client peuvent le modifier"
            )

        email = telephone = fullname = company_name = None

        if request.email is not None:
            try:
                email = Email(request.email)
            except (ValidationError, InvalidEmailError, InvalidPhoneError) as e:
                return UpdateClientResponse(
                    success=False,
                    error=str(e),
                    msg="L'email n'est pas valide"
                )

        if request.telephone is not None:
            try:
                telephone = Telephone(request.telephone)
            except (ValidationError, InvalidEmailError, InvalidPhoneError) as e:
                return UpdateClientResponse(
                    success=False,
                    error=str(e),
                    msg="Le numéro detéléphone n'est pas valide"
                )

        if request.fullname is not None:
            fullname = request.fullname

        if request.company_name is not None:
            company_name = request.company_name

        client.update_info(
            fullname = fullname,
            email = email,
            telephone = telephone,
            company_name = company_name
        )

        updated_client = self.repository.save(client)

        return UpdateClientResponse(success=True, client=updated_client)


#############################################################################
class ClientFilter(Enum):
    MINE = "mine"

@dataclass
class ListClientRequest:
    user_id: int
    list_filter: Optional[ClientFilter]

@dataclass
class ListClientResponse:
    success: bool
    clients: List[Client] = None
    error: Optional[str] = None
    msg: Optional[str] = None


class ListClientUseCase:
    """Use case for listing associated clients"""
    def __init__(self, client_repository: ClientRepository):
        self.repository = client_repository

    def execute(self, request: ListClientRequest) -> ListClientResponse:
        criteres = dict()
        match request.list_filter:
            case ClientFilter.MINE:
                criteres["commercial_contact_id"] = request.user_id

        all_clients = self.repository.find_all(criteres)
        if not all_clients:
            return ListClientResponse(
                success=False,
                error="Ressource",
                msg="Aucun client trouvé"
            )
        return ListClientResponse(success=True, clients=all_clients)

#############################################################################
@dataclass
class GetClientRequest:
    client_id: int

@dataclass
class GetClientResponse:
    success: bool
    client: Optional[Client] = None
    error: Optional[str] = None
    msg: Optional[str] = None


class GetClientUseCase:
    def __init__(self, client_repository: ClientRepository):
        self.repository = client_repository

    def execute(self, request: GetClientRequest):
        client = self.repository.find_by_id(request.client_id)

        if not client:
            return GetClientResponse(
                success=False,
                error="Ressource",
                msg=f"Client non trouvé"
            )

        return GetClientResponse(success=True, client=client)


##############################################################################
@dataclass
class DeleteClientRequest:
    client_id: int
    authorization: RequestPolicy


@dataclass
class DeleteClientResponse:
    success: bool
    error: Optional[str] = None
    msg: Optional[str] = None


class DeleteClientUseCase:
    def __init__(self, client_repository: ClientRepository):
        self.repository = client_repository

    def execute(self, request: DeleteClientRequest):

        policy = UserPolicy(request.authorization)
        if not policy.is_allowed():
            return DeleteClientResponse(
                success=False,
                error="Permission",
                msg="Seuls les membres administrateur peuvent supprimer des clients"
            )

        client = self.repository.find_by_id(request.client_id)
        if not client:
            return DeleteClientResponse(
                success=False,
                error="Ressource",
                msg=f"Client non trouvé"
            )

        self.repository.delete(client.id)
        return DeleteClientResponse(success=True)