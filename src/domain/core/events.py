from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class DomainEvent:
    """Base class for all domain events"""
    id: UUID
    timestamp: datetime = datetime.now()

    def __post_init__(self):
        if not hasattr(self, 'timestamp'):
            self.timestamp = datetime.now()