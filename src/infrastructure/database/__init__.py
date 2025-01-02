from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from typing import Generator
from .models.base import Base

class Database:
    def __init__(self, url: str):
        self._engine = create_engine(url)
        self._session_factory = sessionmaker(bind=self._engine)
        self._scoped_session = scoped_session(self._session_factory)

    def create_database(self):
        """Create all database tables"""
        Base.metadata.create_all(self._engine)

    def drop_database(self):
        """Drop all database tables"""
        Base.metadata.drop_all(self._engine)

    @contextmanager
    def session(self) -> Generator:
        """Provide a transactional scope around a series of operations."""
        session = self._scoped_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @property
    def session_factory(self):
        return self._scoped_session