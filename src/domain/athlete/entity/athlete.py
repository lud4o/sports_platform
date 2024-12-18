from datetime import date
from typing import Optional, List
from uuid import UUID
from domain.core.aggregate_root import AggregateRoot
from .value_objects import Name, EmailAddress, Gender

class Athlete(AggregateRoot):
    def __init__(
        self,
        name: Name,
        birthdate: date,
        gender: Gender,
        sport: str,
        email: Optional[EmailAddress] = None,
        custom_team: Optional[str] = None,
        id: Optional[UUID] = None
    ):
        super().__init__(id)
        self._name = name
        self._birthdate = birthdate
        self._gender = gender
        self._sport = sport
        self._email = email
        self._custom_team = custom_team
        self._activated = False

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self._birthdate.year - (
            (today.month, today.day) < (self._birthdate.month, self._birthdate.day)
        )

    @property
    def age_group(self) -> str:
        """Dynamically calculate age group based on current date"""
        age = self.age
        if age <= 8: return 'U8'
        elif age <= 10: return 'U10'
        elif age <= 12: return 'U12'
        elif age <= 14: return 'U14'
        elif age <= 16: return 'U16'
        elif age <= 18: return 'U18'
        elif age <= 20: return 'U20'
        return '20+'

    @property
    def competitive_age_group(self) -> str:
        """Returns custom team age group if set, otherwise returns natural age group"""
        return self._custom_team or self.age_group

    def set_custom_team(self, age_group: str) -> None:
        """Assign athlete to a custom age group team"""
        valid_age_groups = ['U8', 'U10', 'U12', 'U14', 'U16', 'U18', 'U20', '20+']
        if age_group not in valid_age_groups:
            raise ValueError(f"Invalid age group. Must be one of {valid_age_groups}")
        self._custom_team = age_group

    def remove_custom_team(self) -> None:
        """Remove custom team assignment"""
        self._custom_team = None

    def invite_to_platform(self) -> None:
        """Mark athlete as invited to create profile"""
        if not self._email:
            raise ValueError("Cannot invite athlete without email address")
        # Here we would trigger an invitation event
        self.add_domain_event(AthleteInvitedEvent(self.id))

    def activate_profile(self) -> None:
        """Activate athlete's profile after they've created it"""
        self._activated = True
        self.add_domain_event(AthleteActivatedEvent(self.id))

    @property
    def is_active(self) -> bool:
        return self._activated

    # Properties for basic info access
    @property
    def name(self) -> Name:
        return self._name
    
    @property
    def email(self) -> Optional[EmailAddress]:
        return self._email
    
    @property
    def gender(self) -> Gender:
        return self._gender
    
    @property
    def sport(self) -> str:
        return self._sport