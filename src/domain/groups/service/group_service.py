from typing import List, Optional
from uuid import UUID
from datetime import date
from domain.athlete.entity.athlete import Athlete
from infrastructure.database.repositories.group_repository import GroupRepository

class GroupService:
    def __init__(self, group_repository: GroupRepository):
        self._repository = group_repository

    def assign_natural_group(self, athlete: Athlete) -> Group:
        """Assign athlete to their natural age/sport/gender group"""
        age = athlete.age
        group = self._repository.find_natural_group(
            sport=athlete.sport,
            gender=athlete.gender,
            age=age
        )
        
        if not group:
            # Create new group if doesn't exist
            age_range = self._get_age_range(age)
            group = self._repository.create_group(
                name=f"{athlete.sport} {athlete.gender} {age_range['name']}",
                type="natural",
                sport=athlete.sport,
                gender=athlete.gender,
                age_range={"min": age_range["min"], "max": age_range["max"]},
                is_custom=False
            )
        
        self._repository.add_to_group(athlete.id, group.id, is_primary=True)
        return group

    def assign_custom_group(self, 
                          athlete_id: UUID, 
                          group_id: UUID,
                          maintain_natural: bool = True) -> None:
        """Assign athlete to a custom group"""
        if not maintain_natural:
            # Remove from primary group if requested
            self._repository.remove_primary_group(athlete_id)
        
        # Add to custom group
        self._repository.add_to_group(athlete_id, group_id, is_primary=False)

    def _get_age_range(self, age: int) -> dict:
        """Get age range and group name for given age"""
        ranges = [
            {"min": 0, "max": 12, "name": "U12"},
            {"min": 13, "max": 14, "name": "U14"},
            {"min": 15, "max": 16, "name": "U16"},
            {"min": 17, "max": 18, "name": "U18"},
            {"min": 19, "max": 20, "name": "U20"},
            {"min": 21, "max": 99, "name": "Senior"}
        ]
        
        for range_info in ranges:
            if range_info["min"] <= age <= range_info["max"]:
                return range_info
        
        return ranges[-1]  # Default to Senior