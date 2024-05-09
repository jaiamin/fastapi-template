from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


def get_engine(database_url: str, echo=False) -> Engine:
    """
    Creates and returns a SQLALchemy Engine object for connecting to a database.
    """
    engine = create_engine(database_url, echo=echo)
    return engine


def get_local_session(database_url: str, echo=False) -> sessionmaker:
    """
    Create and return a sessionmaker object for the local database session.
    """
    engine = get_engine(database_url, echo)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session