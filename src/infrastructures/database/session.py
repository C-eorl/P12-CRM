import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.infrastructures.database.models import Base

_engine = None
_SessionLocal = None

def init_engine():
    global _engine, _SessionLocal

    if _engine is not None:
        return

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise EnvironmentError("DATABASE_URL n'est pas valide")

    _engine = create_engine(database_url)
    _SessionLocal = sessionmaker(bind=_engine)

def get_engine():
    if _engine is None:
        init_engine()
    return _engine

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)

def get_session() -> Session:
    if _SessionLocal is None:
        init_engine()
    return _SessionLocal()
