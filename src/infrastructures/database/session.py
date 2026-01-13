import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def init_db():
    """Initialize the database."""
    pass

def get_session() -> Session:
    """Get a database session."""
    with Session(engine) as session:
        return session


if __name__ == "__main__":
    init_db()