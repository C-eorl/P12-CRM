import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
import bcrypt
import jwt

from src.domain.entities.entities import User

load_dotenv()

class BcryptPasswordHasher:

    def hash_password(self, password: str) -> str:
        """Hash a password """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a hashed password """
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


class JWTTokenManager:
    def __init__(self):
        self.expiration = int(os.getenv("JWT_EXPIRATION_HOURS"))
        self.algorithm = "HS256"
        self.secret_key = os.getenv("JWT_SECRET_KEY")

    def create_token(self, user_id: int) -> str:
        """Create a JWT token for user"""
        now = datetime.utcnow()
        payload = {
            'user_id': user_id,
            'iat': int(now.timestamp()),
            'exp': int((now + timedelta(hours=self.expiration)).timestamp()),
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token


    def decode_token(self, token: str) -> Optional[dict]:
        """Decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


class TokenStore:

    TOKEN_DIR = Path(__file__).resolve().parent
    TOKEN_FILE = TOKEN_DIR / "token"

    @classmethod
    def save_token(cls, token: str):
        """Enregistre le token"""
        cls.TOKEN_FILE.write_text(token)

    @classmethod
    def get_token(cls) -> Optional[str]:
        """Récupère le token"""
        if not cls.TOKEN_FILE.exists():
            return None
        return cls.TOKEN_FILE.read_text().strip()

    @classmethod
    def delete_token(cls):
        """Supprime le token"""
        if cls.TOKEN_FILE.exists():
            cls.TOKEN_FILE.unlink()
    @classmethod
    def has_token(cls) -> bool:
        """Vérifie si un token est enregistré"""
        return cls.TOKEN_FILE.exists()