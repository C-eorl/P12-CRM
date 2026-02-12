from src.infrastructures.database.session import get_session
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyUserRepository
from src.infrastructures.security.security import TokenStore, JWTTokenManager


def normalize(value: str) -> str | None:
    return value if value not in ('', 0) else None


def get_current_user() :

    if not TokenStore.has_token():
        return None
    if TokenStore.has_expired():
        TokenStore.delete_token()
        return None

    token = TokenStore.get_token()
    jwt = JWTTokenManager()
    payload = jwt.decode_token(token)

    if payload is None:
        TokenStore.delete_token()
        return None

    repo = SQLAlchemyUserRepository(get_session())
    user = repo.find_by_id(payload["user_id"])
    return {"user_current_id": user.id, "user_current_role": user.role}