"""Authentication interfaces for Epic Events CRM"""
from typing import Optional, Protocol


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

    def decode_token(self, token: str) -> Optional[dict]: ...
