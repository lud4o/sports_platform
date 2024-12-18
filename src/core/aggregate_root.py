from .entity import Entity
from typing import List

class AggregateRoot(Entity):
    def __init__(self):
        super().__init__()
        self._domain_events: List = []

    def add_domain_event(self, event: 'DomainEvent'):
        self._domain_events.append(event)

    def clear_domain_events(self):
        self._domain_events.clear()

    @property
    def domain_events(self) -> List['DomainEvent']:
        return self._domain_events
