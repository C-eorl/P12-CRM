from dataclasses import dataclass
from typing import Optional, List

from src.domain.entities.entities import User
from src.domain.entities.enums import Role
from src.domain.entities.exceptions import InvalidEmailError, ValidationError
from src.domain.entities.value_objects import Email
from src.domain.interfaces.auth import PasswordHasherInterface
from src.domain.interfaces.repository import UserRepository
from src.domain.policies.user_policy import UserPolicy

################################################################################################
@dataclass
class CreateUserRequest:
    """Request to create a new client"""
    fullname: str
    email: str
    password: str
    role: str
    current_user: User


@dataclass
class CreateUserResponse:
    """Response to create a new client"""
    success: bool
    user: Optional[User] = None
    error: Optional[str] = None


class CreateClientUseCase:
    """Use case for creating a new client"""

    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasherInterface):
        self.repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, request: CreateUserRequest) -> CreateUserResponse:

        policy = UserPolicy(request.current_user)

        if not policy.can_create_client():
            return CreateUserResponse(
                success=False,
                error="Seuls les membres gestion peuvent créer des utilisateurs"
            )

        try:
            email = Email(request.email)
        except (ValidationError, InvalidEmailError) as e:
            return CreateUserResponse(success=False, error=str(e))

        hashed_password = self.password_hasher.hash_password(request.password)

        client = User(
            id = None,
            fullname=request.fullname,
            email = email,
            password= hashed_password,
            role = Role(request.role),
        )
        saved_client = self.repository.save(client)

        return CreateUserResponse(success=True, user=saved_client)

################################################################################################
@dataclass
class UpdateUserRequest:
    user_id: int
    fullname: Optional[str]
    email: Optional[str]
    # password
    # role
    current_user: User


@dataclass
class UpdateUserResponse:
    success: bool
    user: Optional[User] = None
    error: Optional[str] = None


class UpdateClientUseCase:
    """
    Use case for updating associated client.
    """
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def execute(self, request: UpdateUserRequest):
        # Permission liée au role
        policy = UserPolicy(request.current_user)
        if not policy.can_update_client():
            return UpdateUserResponse(
                success=False,
                error="Seuls les membres commerciaux peuvent modifier des clients"
            )

        user = self.repository.find_by_id(request.user_id)
        if not user:
            return UpdateUserResponse(
                success=False,
                error=f"Client non trouvé"
            )

        email = fullname = None

        if request.email is not None:
            try:
                email = Email(request.email)
            except (ValidationError, InvalidEmailError) as e:
                return UpdateUserResponse(success=False, error=str(e))

        if request.fullname is not None:
            fullname = request.fullname


        user.update_info(
            fullname = fullname,
            email = email,
        )

        updated_client = self.repository.save(user)

        return UpdateUserResponse(success=True, user=updated_client)

################################################################################################

@dataclass
class ListUserResponse:
    success: bool
    users: List[User] = None
    error: Optional[str] = None


class ListUserUseCase:
    """Use case for listing associated clients"""
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def execute(self) -> ListUserResponse:
        all_user = self.repository.find_all()
        return ListUserResponse(success=True, users=all_user)


#############################################################################
@dataclass
class GetUserRequest:
    user_id: int
    current_user: User


@dataclass
class GetUserResponse:
    success: bool
    user: Optional[User] = None
    error: Optional[str] = None


class GetClientUseCase:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def execute(self, request: GetUserRequest):
        user = self.repository.find_by_id(request.user_id)

        if not user:
            return GetUserResponse(
                success=False,
                error=f"Utilisateur non trouvé"
            )

        return GetUserResponse(success=True, user=user)


##############################################################################
@dataclass
class DeleteUserRequest:
    user_id: int
    current_user: User


@dataclass
class DeleteUserResponse:
    success: bool
    error: Optional[str] = None


class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def execute(self, request: DeleteUserRequest):

        policy = UserPolicy(request.current_user)
        if not policy.can_delete_client():
            return DeleteUserResponse(
                success=False,
                error="Seuls les membres gestions peuvent supprimer des utilisateurs"
            )

        user = self.repository.find_by_id(request.user_id)
        if not user:
            return DeleteUserResponse(
                success=False,
                error=f"Utilisateur non trouvé"
            )


        self.repository.delete(user.id)
        return DeleteUserResponse(success=True)