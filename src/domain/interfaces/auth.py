"""Authentication interfaces for Epic Events CRM"""
from typing import Optional, Protocol

from src.domain.entities.entities import User


class PasswordHasherInterface(Protocol):
    """
    Interface for password hashers
    - hash_password : Hash a password
    - verify_password : Verify a password
    """

    def hash_password(self, password: str) -> str: ...

    def verify_password(self, password: str, hashed: str) -> bool: ...


class TokenManagerInterface(Protocol):
    """
    Interface for token managers
    - create_token : Create a new token for a user
    -decode_token : Decode an existing token and return id user
    """

    def create_token(self, user_id: int) -> str: ...

    def decode_token(self, token: str) -> Optional[int]: ...


class AuthServiceInterface(Protocol):
    """
    Interface for authentification service
    - authenticate : Authenticate a user and return token
    - get_current_user : Get current user from token
    """

    def authenticate(self, email: str, password: str) -> Optional[str]: ...

    def get_current_user(self, token: str) -> Optional[User]: ...