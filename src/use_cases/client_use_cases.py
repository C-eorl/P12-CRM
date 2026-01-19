from dataclasses import dataclass
from typing import Optional, List


from src.domain.entities.entities import Client, User
from src.domain.entities.exceptions import ValidationError, InvalidEmailError, InvalidPhoneError
from src.domain.entities.value_objects import Email, Telephone

from src.domain.interfaces.repository import ClientRepository
from src.domain.policies.user_policy import UserPolicy


################################################################################################
@dataclass
class CreateClientRequest:
    """Request to create a new client"""
    fullname: str
    email: str
    telephone: str
    company_name: str
    current_user: User


@dataclass
class CreateClientResponse:
    """Response to create a new client"""
    success: bool
    client: Optional[Client] = None
    error: Optional[str] = None


class CreateClientUseCase:
    """Use case for creating a new client"""

    def __init__(self, client_repository: ClientRepository):
        self.repository = client_repository

    def execute(self, request: CreateClientRequest) -> CreateClientResponse:

        policy = UserPolicy(request.current_user)

        if not policy.can_create_client():
            return CreateClientResponse(
                success=False,
                error="Seuls les membres commerciaux peuvent créer des clients"
            )

        try:
            email = Email(request.email)
            telephone = Telephone(request.telephone)
        except (ValidationError, InvalidEmailError, InvalidPhoneError) as e:
            return CreateClientResponse(success=False, error=str(e))

        client = Client(
            id = None,
            fullname=request.fullname,
            email = email,
            telephone = telephone,
            company_name=request.company_name,
            commercial_contact_id=request.current_user.id
        )
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
    current_user: User


@dataclass
class UpdateClientResponse:
    success: bool
    client: Optional[Client] = None
    error: Optional[str] = None


class UpdateClientUseCase:
    """
    Use case for updating associated client.
    """
    def __init__(self, client_repository: ClientRepository):
        self.repository = client_repository

    def execute(self, request: UpdateClientRequest):
        # Permission liée au role
        policy = UserPolicy(request.current_user)
        if not policy.can_update_client():
            return UpdateClientResponse(
                success=False,
                error="Seuls les membres commerciaux peuvent modifier des clients"
            )

        client = self.repository.find_by_id(request.client_id)
        if not client:
            return UpdateClientResponse(
                success=False,
                error=f"Client non trouvé"
            )

        # Permission liée à l'association
        if request.current_user.id != client.commercial_contact_id:
            return UpdateClientResponse(
                success=False,
                error="Vous n'êtes pas associé au client"
            )

        email = telephone = fullname = company_name = None

        if request.email is not None:
            try:
                email = Email(request.email)
            except (ValidationError, InvalidEmailError, InvalidPhoneError) as e:
                return UpdateClientResponse(success=False, error=str(e))

        if request.telephone is not None:
            try:
                telephone = Telephone(request.telephone)
            except (ValidationError, InvalidEmailError, InvalidPhoneError) as e:
                return UpdateClientResponse(success=False, error=str(e))

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

@dataclass
class ListClientResponse:
    success: bool
    clients: List[Client] = None
    error: Optional[str] = None


class ListClientUseCase:
    """Use case for listing associated clients"""
    def __init__(self, client_repository: ClientRepository):
        self.repository = client_repository

    def execute(self) -> ListClientResponse:
        try:
            all_client = self.repository.find_all()
            return ListClientResponse(success=True, clients=all_client)

        except Exception as e:
            return ListClientResponse(success=False, error=str(e))
#############################################################################
@dataclass
class GetClientRequest:
    client_id: int
    current_user: User


@dataclass
class GetClientResponse:
    success: bool
    client: Optional[Client] = None
    error: Optional[str] = None


class GetClientUseCase:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def execute(self, request: GetClientRequest):
        try:
            client = self.repository.find_by_id(request.client_id)

            if not client:
                return GetClientResponse(
                    success=False,
                    error=f"Client non trouvé"
                )

            return GetClientResponse(success=True, client=client)

        except Exception as e:
            return GetClientResponse(
                success=False,
                error=f"Erreur lors de la recherche: {str(e)}"
            )

##############################################################################
@dataclass
class DeleteClientRequest:
    client_id: int
    current_user: User


@dataclass
class DeleteClientResponse:
    success: bool
    error: Optional[str] = None


class DeleteClientUseCase:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def execute(self, request: DeleteClientRequest):

        policy = UserPolicy(request.current_user)

        try:
            client = self.repository.find_by_id(request.client_id)

            if not policy.can_delete_client():
                return DeleteClientResponse(
                    success=False,
                    error="Seuls les membres commerciaux peuvent supprimer des clients"
                )

            if not client:
                return DeleteClientResponse(
                    success=False,
                    error=f"Client non trouvé"
                )


            self.repository.delete(client.id)
            return DeleteClientResponse(success=True)

        except Exception as e:
            return DeleteClientResponse(
                success=False,
                error=f"Erreur lors de la recherche: {str(e)}"
            )