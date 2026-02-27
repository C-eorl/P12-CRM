from pathlib import Path

from src.infrastructures.database.session import get_session
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyUserRepository
from src.infrastructures.security.security import TokenStore, JWTTokenManager


def normalize(value):
    """
    Normalize default value
    :param value: value to normalize
    :return: value or None
    """
    return value if value not in ('', 0) else None


def get_current_user() :
    """
    Get current user via jwt token
    :return: dict or None
    """
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

def init_environment():
    """
    Initialize environment variable file
    :return: True if initialization was successful, False otherwise
    """
    ENV_PATH = Path(".env")

    DEFAULT_ENV = {
        "DATABASE_URL": "",

        "JWT_SECRET_KEY": "votre-cle-secret",
        "JWT_ALGORITHM": "HS256",
        "JWT_EXPIRATION_HOURS": "8",

        "SENTRY_DSN": "",
    }

    if ENV_PATH.exists():
        return False

    with ENV_PATH.open("w") as f:
        for key, value in DEFAULT_ENV.items():
            f.write(f"{key}={value}\n")
    return True
