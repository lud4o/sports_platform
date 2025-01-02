from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from ..core.events import DomainEvent

@dataclass
class AthleteInvitedEvent:
    """Event raised when an athlete is invited to the platform"""
    athlete_id: UUID
    timestamp: datetime = datetime.now()

@dataclass
class AthleteActivatedEvent:
    """Event raised when an athlete activates their account"""
    athlete_id: UUID
    timestamp: datetime = datetime.now()

    