from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models.base import Base

class DatabaseConfig:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        """Drop all database tables"""
        Base.metadata.drop_all(self.engine)

    def get_session(self):
        """Get a new database session"""
        return self.Session()