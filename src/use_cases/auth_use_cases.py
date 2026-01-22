from dataclasses import dataclass
from typing import Optional

from src.domain.interfaces.auth import PasswordHasherInterface, TokenManagerInterface
from src.domain.interfaces.repository import UserRepository
from src.infrastructures.security.security import TokenStore


@dataclass
class AuthenticateRequest:
    email: str
    password: str

@dataclass
class AuthenticateResponse:
    success: bool
    error: Optional[str] = None

class AuthenticateUseCase:
    def __init__(self,
                 repository: UserRepository,
                 password_hasher: PasswordHasherInterface,
                 token_manager: TokenManagerInterface
                 ):
        self.repo = repository
        self.password_hasher = password_hasher
        self.token_manager = token_manager

    def execute(self, request: AuthenticateRequest):

        user = self.repo.find_by_email(request.email)
        if not user:
            return AuthenticateResponse(
                success=False,
                error="Email ou mot de passe incorrect"
            )

        if not self.password_hasher.verify_password(request.password, user.password):
            return AuthenticateResponse(
                success=False,
                error="Email ou mot de passe incorrect"
            )

        token = self.token_manager.create_token(user.id)
        TokenStore.save_token(token)

        return AuthenticateResponse(
            success=True,
        )