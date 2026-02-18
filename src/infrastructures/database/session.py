import os

import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.infrastructures.database.models import Base

_engine = None
_SessionLocal = None

def init_engine(force=False):
    """
    Initialize the database engine
    :param force: force the engine to be initialized
    :return:
    """
    global _engine, _SessionLocal

    if _engine is not None and not force:
        return

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise EnvironmentError("DATABASE_URL n'est pas valide")

    _engine = create_engine(database_url)
    _SessionLocal = sessionmaker(bind=_engine)

def get_engine():
    """
    Get a database engine instance or create it if it doesn't exist
    :return:
    """
    if _engine is None:
        init_engine()
    return _engine


def init_db():
    """
    Initialize the table database
    :return:
    """
    engine = get_engine() if _engine else None
    init_engine(force=True)   # Force la recréation avec la nouvelle URL
    engine = get_engine()
    Base.metadata.create_all(engine)

def get_session() -> Session:
    """
    Get a database session
    :return: Session
    """
    if _SessionLocal is None:
        init_engine()
    return _SessionLocal()

def init_postgresql(user, password, db_name):
    """
    Initialize the DB or create it if it doesn't exist
    :param user: username postgres
    :param password: password postgres
    :param db_name: name of the database
    :return: True or False
    """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host="localhost",
            port="5432",
        )
        conn.autocommit =True
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s;",
            (db_name,)
        )
        exist_db = cursor.fetchone()

        if exist_db:
            return False
        else:
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(db_name)
                    )
            )
            cursor.close()
            conn.close()
            return True
    except Exception as e:
        raise e