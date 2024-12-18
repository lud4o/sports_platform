from typing import Optional
from uuid import UUID
from domain.core.aggregate_root import AggregateRoot
from domain.athlete.entity.value_objects import Gender

class Benchmark(AggregateRoot):
    def __init__(
        self,
        test_id: UUID,
        value: float,
        gender: Gender,
        age_group: str,
        sport: str,
        is_normative: bool = False,
        source: Optional[str] = None,
        id: Optional[UUID] = None
    ):
        super().__init__(id)
        self._test_id = test_id
        self._value = value
        self._gender = gender
        self._age_group = age_group
        self._sport = sport
        self._is_normative = is_normative
        self._source = source

    @property
    def value(self) -> float:
        return self._value

    @property
    def is_normative(self) -> bool:
        return self._is_normative