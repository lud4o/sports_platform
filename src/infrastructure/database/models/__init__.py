from .base import Base, BaseModel
from .group import Group, AthleteGroup
from .test import TestDefinition, TestResult, TestAnalysis
from .anthropometric import AnthropometricData
from .athlete import Athlete
from .batch import BatchOperation
from src.interfaces.web import db

# Import indexes after all models are defined
from .indexes import create_indexes

__all__ = [
    'Base',
    'BaseModel',
    'Athlete',
    'Group',
    'AthleteGroup',
    'TestDefinition',
    'TestResult',
    'TestAnalysis',
    'AnthropometricData',
    'BatchOperation',
    'create_indexes'
]

# Register index creation event
from sqlalchemy import event
@event.listens_for(Base.metadata, 'after_create')
def create_db_indexes(target, connection, **kw):
    """Create all indexes after database creation"""
    indexes = create_indexes()
    for index in indexes:
        index.create(connection)