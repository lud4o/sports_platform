from sqlalchemy import Index
from .test import TestResult
from .batch import BatchOperation
from .athlete import Athlete
from .group import Group

def create_indexes():
    """Create all database indexes"""
    return [
        # Test Results indexes
        Index('idx_test_results_date', TestResult.test_date.desc()),
        Index('idx_test_results_athlete_test', 
              TestResult.athlete_id, 
              TestResult.test_definition_id),
        
        # Batch Operations indexes
        Index('idx_batch_operations_status', BatchOperation.status),
        
        # Athlete indexes
        Index('idx_athlete_sport', Athlete.sport),
        Index('idx_athlete_birthdate', Athlete.birthdate),
        Index('idx_athlete_name', Athlete.last_name, Athlete.first_name),
        
        # Group indexes
        Index('idx_group_type', Group.type),
        Index('idx_group_sport_gender', Group.sport, Group.gender)
        
    ]