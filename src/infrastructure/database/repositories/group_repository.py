from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import Integer
from ..models.group import Group, AthleteGroup
from ..models.athlete import Athlete

class GroupRepository:
    def __init__(self, session: Session):
        self._session = session

    def find_natural_group(self, sport: str, gender: str, age: int) -> Optional[Group]:
        """Find natural group for given attributes"""
        return self._session.query(Group)\
            .filter(Group.sport == sport)\
            .filter(Group.gender == gender)\
            .filter(Group.is_custom == False)\
            .filter(
                (Group.age_range['min'].astext.cast(Integer) <= age) &
                (Group.age_range['max'].astext.cast(Integer) >= age)
            ).first()

    def add_to_group(self, athlete_id: UUID, group_id: UUID, is_primary: bool = True) -> None:
        """Add athlete to group"""
        # Check if membership already exists
        existing = self._session.query(AthleteGroup)\
            .filter(AthleteGroup.athlete_id == athlete_id)\
            .filter(AthleteGroup.group_id == group_id)\
            .first()
            
        if existing:
            existing.is_primary = is_primary
        else:
            membership = AthleteGroup(
                athlete_id=athlete_id,
                group_id=group_id,
                is_primary=is_primary
            )
            self._session.add(membership)
        
        self._session.commit()

    def remove_primary_group(self, athlete_id: UUID) -> None:
        """Remove athlete from their primary group"""
        self._session.query(AthleteGroup)\
            .filter(AthleteGroup.athlete_id == athlete_id)\
            .filter(AthleteGroup.is_primary == True)\
            .delete()
        self._session.commit()

    def get_athlete_groups(self, athlete_id: UUID) -> List[Group]:
        """Get all groups for an athlete"""
        return self._session.query(Group)\
            .join(AthleteGroup)\
            .filter(AthleteGroup.athlete_id == athlete_id)\
            .all()

    def get_group_athletes(self, group_id: UUID) -> List[Athlete]:
        """Get all athletes in a group"""
        return self._session.query(Athlete)\
            .join(AthleteGroup)\
            .filter(AthleteGroup.group_id == group_id)\
            .all()

    def create_group(self, 
                    name: str,
                    type: str,
                    sport: str,
                    gender: str,
                    age_range: dict,
                    is_custom: bool = False) -> Group:
        """Create a new group"""
        group = Group(
            name=name,
            type=type,
            sport=sport,
            gender=gender,
            age_range=age_range,
            is_custom=is_custom
        )
        self._session.add(group)
        self._session.commit()
        return group