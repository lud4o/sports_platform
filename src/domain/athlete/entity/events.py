from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class AthleteInvitedEvent:
    athlete_id: UUID
    timestamp: datetime = datetime.now()

@dataclass
class AthleteActivatedEvent:
    athlete_id: UUID
    timestamp: datetime = datetime.now()