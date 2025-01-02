from uuid import UUID
from typing import List
from datetime import datetime

class AggregateRoot:
    def __init__(self, id: UUID = None):
        self._id = id or UUID()
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        self._domain_events: List = []

    def add_domain_event(self, event: 'DomainEvent'):
        self._domain_events.append(event)

    def clear_domain_events(self):
        self._domain_events.clear()

    @property
    def domain_events(self) -> List['DomainEvent']:
        return self._domain_events
