from datetime import date
import uuid
from src.interfaces.web import db  # Import SQLAlchemy instance
from sqlalchemy import Column, String, Date, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from ....domain.athlete.value_objects import Gender

class Athlete(db.Model):
    __tablename__ = 'athletes'
    
    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    sport = Column(String, nullable=False)
    email = Column(String)
    is_active = Column(Boolean, default=False)
    
    test_results = db.relationship("TestResult", back_populates="athlete", lazy="dynamic", cascade="all, delete-orphan")
    anthropometric_data = db.relationship("AnthropometricData", back_populates="athlete", cascade="all, delete-orphan")
    groups = db.relationship("Group", secondary="athlete_groups", back_populates="athletes")

    def __repr__(self):
        return f'<Athlete {self.first_name} {self.last_name}>'

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.birthdate.year - (
            (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
        )

    @property
    def age_group(self) -> str:
        """Calculate age group based on current age"""
        age = self.age
        if age <= 12: return 'U12'
        elif age <= 14: return 'U14'
        elif age <= 16: return 'U16'
        elif age <= 18: return 'U18'
        elif age <= 20: return 'U20'
        return 'Senior'

    def to_entity(self) -> 'AthleteEntity':
        """Convert DB model to domain entity"""
        from ....domain.athlete.entity.athlete import Athlete as AthleteEntity
        from ....domain.athlete.value_objects import Name, EmailAddress
        
        return AthleteEntity(
            id=self.id,
            name=Name(self.first_name, self.last_name),
            birthdate=self.birthdate,
            gender=self.gender,
            sport=self.sport,
            email=EmailAddress(self.email) if self.email else None,
            custom_team=self.custom_team
        )

    @classmethod
    def from_entity(cls, athlete: 'AthleteEntity') -> 'Athlete':
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