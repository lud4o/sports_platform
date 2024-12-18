from typing import List, Optional
from uuid import UUID
from domain.core.aggregate_root import AggregateRoot
from .value_objects import TestCategory, TestUnit, TestProtocol, AdditionalVariable

class Test(AggregateRoot):
    def __init__(
        self,
        name: str,
        category: TestCategory,
        primary_unit: TestUnit,
        description: Optional[str] = None,
        protocol: Optional[TestProtocol] = None,
        additional_variables: List[AdditionalVariable] = None,
        id: Optional[UUID] = None
    ):
        super().__init__(id)
        self._name = name
        self._category = category
        self._primary_unit = primary_unit
        self._description = description
        self._protocol = protocol
        self._additional_variables = additional_variables or []

    @property
    def name(self) -> str:
        return self._name

    @property
    def category(self) -> TestCategory:
        return self._category

    @property
    def primary_unit(self) -> TestUnit:
        return self._primary_unit

    @property
    def additional_variables(self) -> List[AdditionalVariable]:
        return self._additional_variables.copy()

class SpeedTest(Test):
    def __init__(self, name: str, description: Optional[str] = None, id: Optional[UUID] = None):
        super().__init__(
            name=name,
            category=TestCategory.SPEED,
            primary_unit=TestUnit.SECONDS,
            description=description,
            id=id
        )

class PowerTest(Test):
    def __init__(
        self, 
        name: str, 
        primary_unit: TestUnit,
        description: Optional[str] = None,
        additional_variables: List[AdditionalVariable] = None,
        id: Optional[UUID] = None
    ):
        super().__init__(
            name=name,
            category=TestCategory.POWER,
            primary_unit=primary_unit,
            description=description,
            additional_variables=additional_variables,
            id=id
        )

# Create test result entity to store test results
from datetime import datetime
from enum import Enum

class TestPhase(Enum):
    DAILY = "daily_monitoring"
    WEEKLY = "weekly_monitoring"
    CYCLE_END = "training_cycle_end"

class TestResult(AggregateRoot):
    def __init__(
        self,
        athlete_id: UUID,
        test_id: UUID,
        value: float,
        test_date: datetime,
        phase: TestPhase,
        additional_values: dict = None,
        id: Optional[UUID] = None
    ):
        super().__init__(id)
        self._athlete_id = athlete_id
        self._test_id = test_id
        self._value = value
        self._test_date = test_date
        self._phase = phase
        self._additional_values = additional_values or {}

    @property
    def value(self) -> float:
        return self._value

    @property
    def test_date(self) -> datetime:
        return self._test_date

    @property
    def phase(self) -> TestPhase:
        return self._phase

    @property
    def additional_values(self) -> dict:
        return self._additional_values.copy()