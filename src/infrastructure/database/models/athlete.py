from datetime import date
from sqlalchemy import Column, String, Date, Boolean, Enum
from sqlalchemy.orm import relationship
from ..base import BaseModel
from domain.athlete.entity.value_objects import Gender

class AthleteModel(BaseModel):
    __tablename__ = 'athletes'

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birthdate = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    sport = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    custom_team = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=False)

    # Relationships will be added here later
    test_results = relationship("TestResultModel", back_populates="athlete")
    group_memberships = relationship("GroupMembershipModel", back_populates="athlete")

    def to_entity(self) -> Athlete:
        """Convert DB model to domain entity"""
        return Athlete(
            id=self.id,
            name=Name(self.first_name, self.last_name),
            birthdate=self.birthdate,
            gender=self.gender,
            sport=self.sport,
            email=EmailAddress(self.email) if self.email else None,
            custom_team=self.custom_team
        )

    @classmethod
    def from_entity(cls, athlete: Athlete) -> 'AthleteModel':
        """Create DB model from domain entity"""
        return cls(
            id=athlete.id,
            first_name=athlete.name.first_name,
            last_name=athlete.name.last_name,
            birthdate=athlete.birthdate,
            gender=athlete.gender,
            sport=athlete.sport,
            email=athlete.email.value if athlete.email else None,
            custom_team=athlete.custom_team,
            is_active=athlete.is_active
        )