from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from config import settings

DATABASE_URL = settings.DATABASE_URL

non_autocommit_engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_size=settings.DB_POOL_SIZE,
    pool_recycle=settings.DB_POOL_RECYCLE,
)
autocommit_engine = non_autocommit_engine.execution_options(
    isolation_level="AUTOCOMMIT"
)

Base = declarative_base()

NonAutoCommitSession = sessionmaker(bind=non_autocommit_engine)
AutoCommitSession = sessionmaker(bind=autocommit_engine)


def get_non_autocommit_db() -> Session:
    """
    Use this engine for writing to the database.
    """
    db = NonAutoCommitSession()
    try:
        yield db
    finally:
        db.close()


def get_autocommit_db() -> Session:
    """
    Use this engine for reading from the database.
    """
    db = AutoCommitSession()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_non_autocommit_db_contextmanager() -> Session:
    """
    Use this engine for writing to the database.
    """
    db = NonAutoCommitSession()
    try:
        yield db
    finally:
        db.close()
