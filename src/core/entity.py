from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

class Entity:
    def __init__(self, id: Optional[UUID] = None):
        self._id = id or uuid4()
        self._created_at = datetime.now()
        self._updated_at = datetime.now()

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at
