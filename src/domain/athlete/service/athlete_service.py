from typing import List, Optional
from ..entity.athlete import Athlete
from ..entity.value_objects import Name, EmailAddress, Gender
from ..repository.athlete_repository import AthleteRepository

class AthleteService:
    def __init__(self, repository: AthleteRepository):
        self._repository = repository

    def create_athlete(self, 
                      first_name: str,
                      last_name: str,
                      birthdate: date,
                      gender: str,
                      sport: str,
                      email: Optional[str] = None) -> Athlete:
        """Create a new athlete"""
        name = Name(first_name=first_name, last_name=last_name)
        
        # Check if athlete already exists
        existing = self._repository.find_by_name(name)
        if existing:
            raise ValueError(f"Athlete {name} already exists")

        # Create email address if provided
        email_address = EmailAddress(email) if email else None
        
        # Create athlete
        athlete = Athlete(
            name=name,
            birthdate=birthdate,
            gender=Gender(gender.lower()),
            sport=sport,
            email=email_address
        )

        return self._repository.save(athlete)

    def assign_custom_team(self, athlete_id: UUID, age_group: str) -> Athlete:
        """Assign athlete to a custom age group team"""
        athlete = self._repository.get(athlete_id)
        if not athlete:
            raise ValueError(f"Athlete with id {athlete_id} not found")

        athlete.set_custom_team(age_group)
        return self._repository.save(athlete)

    def invite_athlete(self, athlete_id: UUID) -> None:
        """Invite athlete to create profile"""
        athlete = self._repository.get(athlete_id)
        if not athlete:
            raise ValueError(f"Athlete with id {athlete_id} not found")

        athlete.invite_to_platform()
        self._repository.save(athlete)

    def find_team_members(self, 
                         age_group: str,
                         include_custom_teams: bool = True) -> List[Athlete]:
        """Find all athletes in a specific age group"""
        athletes = self._repository.find_by_criteria(age_group=age_group)
        
        if include_custom_teams:
            custom_team_athletes = self._repository.find_by_criteria(custom_team=age_group)
            athletes.extend(custom_team_athletes)

        return athletes

    def find_similar_athletes(self, athlete_id: UUID) -> List[Athlete]:
        """Find athletes similar to the given athlete"""
        athlete = self._repository.get(athlete_id)
        if not athlete:
            raise ValueError(f"Athlete with id {athlete_id} not found")

        return self._repository.find_by_criteria(
            age_group=athlete.age_group,
            gender=athlete.gender,
            sport=athlete.sport
        )