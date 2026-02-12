from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

from src.domain.entities.entities import User
from src.domain.entities.enums import Role
from src.domain.entities.exceptions import InvalidEmailError, ValidationError
from src.domain.entities.value_objects import Email
from src.domain.interfaces.auth import PasswordHasherInterface
from src.domain.interfaces.repository import UserRepository
from src.domain.policies.user_policy import UserPolicy, RequestPolicy


################################################################################################
@dataclass
class CreateUserRequest:
    """Request to create a new client"""
    fullname: str
    email: str
    password: str
    role: Role
    authorization : RequestPolicy


@dataclass
class CreateUserResponse:
    """Response to create a new client"""
    success: bool
    user: Optional[User] = None
    error: Optional[str] = None
    msg: Optional[str] = None


class CreateUserUseCase:
    """Use case for creating a new client"""

    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasherInterface):
        self.repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, request: CreateUserRequest) -> CreateUserResponse:

        policy = UserPolicy(request.authorization)
        if not policy.is_allowed():
            return CreateUserResponse(
                success=False,
                error="Permission",
                msg="Seuls les membres gestion peuvent créer des utilisateurs"
            )

        try:
            email = Email(request.email)
        except (ValidationError, InvalidEmailError) as e:
            return CreateUserResponse(
                success=False,
                error=str(e),
                msg="Email non valide"
            )

        hashed_password = self.password_hasher.hash_password(request.password)

        user = User(
            id = None,
            fullname=request.fullname,
            email = email,
            password= hashed_password,
            role = Role(request.role),
        )
        saved_user = self.repository.save(user)

        return CreateUserResponse(success=True, user=saved_user)

################################################################################################
@dataclass
class UpdateUserRequest:
    user_id: int
    fullname: Optional[str]
    email: Optional[str]
    authorization : RequestPolicy


@dataclass
class UpdateUserResponse:
    success: bool
    user: Optional[User] = None
    error: Optional[str] = None
    msg: Optional[str] = None


class UpdateUserUseCase:
    """
    Use case for updating associated client.
    """
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def execute(self, request: UpdateUserRequest):
        # Permission liée au role
        policy = UserPolicy(request.authorization)
        if not policy.is_allowed():
            return UpdateUserResponse(
                success=False,
                error="Permission",
                msg="Seuls les membres gestion peuvent modifier des clients"
            )

        user = self.repository.find_by_id(request.user_id)
        if not user:
            return UpdateUserResponse(
                success=False,
                error="Ressource",
                msg=f"Client non trouvé"
            )

        email = fullname = None

        if request.email is not None:
            try:
                email = Email(request.email)
            except (ValidationError, InvalidEmailError) as e:
                return UpdateUserResponse(
                    success=False,
                    error=str(e),
                    msg="Email non valide"
                )

        if request.fullname is not None:
            fullname = request.fullname


        user.update_info(
            fullname = fullname,
            email = email,
        )

        updated_user = self.repository.save(user)

        return UpdateUserResponse(success=True, user=updated_user)

################################################################################################
class UserFilter(Enum):
    ROLE_COMMERCIAL = "role:commercial"
    ROLE_SUPPORT = "role:support"
    ROLE_GESTION = "role:gestion"
    ROLE_ADMIN = "role:admin"

@dataclass
class ListUserRequest:
    list_filter: Optional[UserFilter]

@dataclass
class ListUserResponse:
    success: bool
    users: List[User] = None
    error: Optional[str] = None
    msg: Optional[str] = None


class ListUserUseCase:
    """Use case for listing associated clients"""
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def execute(self, request: ListUserRequest) -> ListUserResponse:
        criteres = {"role" : None}
        match request.list_filter:
            case UserFilter.ROLE_COMMERCIAL : criteres["role"] = Role.COMMERCIAL
            case UserFilter.ROLE_GESTION : criteres["role"] = Role.GESTION
            case UserFilter.ROLE_SUPPORT : criteres["role"] = Role.SUPPORT
            case UserFilter.ROLE_ADMIN : criteres["role"] = Role.ADMIN

        all_user = self.repository.find_all(criteres)
        if not all_user:
            return ListUserResponse(
                success=False,
                error="Ressource",
                msg="Aucun utilisateur trouvé"
            )

        return ListUserResponse(success=True, users=all_user)


#############################################################################
@dataclass
class GetUserRequest:
    user_id: int


@dataclass
class GetUserResponse:
    success: bool
    user: Optional[User] = None
    error: Optional[str] = None
    msg: Optional[str] = None


class GetUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def execute(self, request: GetUserRequest):
        user = self.repository.find_by_id(request.user_id)

        if not user:
            return GetUserResponse(
                success=False,
                error="Ressource",
                msg=f"Utilisateur non trouvé"
            )

        return GetUserResponse(success=True, user=user)


##############################################################################
@dataclass
class DeleteUserRequest:
    user_id: int
    authorization: RequestPolicy

@dataclass
class DeleteUserResponse:
    success: bool
    error: Optional[str] = None
    msg: Optional[str] = None


class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def execute(self, request: DeleteUserRequest):

        policy = UserPolicy(request.authorization)
        if not policy.is_allowed():
            return DeleteUserResponse(
                success=False,
                error="Permission",
                msg="Seuls les membres gestions peuvent supprimer des utilisateurs"
            )

        user = self.repository.find_by_id(request.user_id)
        if not user:
            return DeleteUserResponse(
                success=False,
                error="Ressource",
                msg=f"Utilisateur non trouvé"
            )

        self.repository.delete(user.id)
        return DeleteUserResponse(success=True)