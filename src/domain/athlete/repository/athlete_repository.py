from abc import abstractmethod
from typing import List, Optional
from uuid import UUID
from domain.core.repository import Repository
from ..entity.athlete import Athlete
from ..entity.value_objects import Name, Gender

class AthleteRepository(Repository[Athlete]):
    @abstractmethod
    def find_by_name(self, name: Name) -> Optional[Athlete]:
        """Find athlete by their full name"""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Athlete]:
        """Find athlete by email address"""
        pass

    @abstractmethod
    def find_by_criteria(self, 
                        age_group: Optional[str] = None,
                        gender: Optional[Gender] = None,
                        sport: Optional[str] = None,
                        custom_team: Optional[str] = None) -> List[Athlete]:
        """Find athletes matching specified criteria"""
        pass

    @abstractmethod
    def find_active(self) -> List[Athlete]:
        """Find all athletes with activated profiles"""
        pass