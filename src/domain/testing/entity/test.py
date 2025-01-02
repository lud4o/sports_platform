from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime
from ...core.aggregate_root import AggregateRoot
from .value_objects import TestCategory, TestUnit, TestProtocol, AdditionalVariable, TestPhase  # Add TestPhase here

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
    def description(self) -> Optional[str]:
        return self._description

    @property
    def protocol(self) -> Optional[TestProtocol]:
        return self._protocol

    @property
    def additional_variables(self) -> List[AdditionalVariable]:
        return self._additional_variables.copy()

    def validate_result(self, value: float, variable_name: Optional[str] = None) -> bool:
        """Validate test result value"""
        if not isinstance(value, (int, float)):
            return False
            
        if variable_name:
            variable = next(
                (var for var in self._additional_variables if var.name == variable_name),
                None
            )
            if not variable:
                return False
                
            if variable.min_value is not None and value < variable.min_value:
                return False
            if variable.max_value is not None and value > variable.max_value:
                return False
                
        return True

    def calculate_derived_variables(self, primary_value: float, additional_values: Dict) -> Dict:
        """Calculate any derived variables based on test results"""
        derived = {}
        
        for variable in self._additional_variables:
            if variable.calculation_formula and variable.dependent_variables:
                if all(dep in additional_values for dep in variable.dependent_variables):
                    # Here you would implement the actual calculation
                    # This is a placeholder
                    derived[variable.name] = 0.0
                
        return derived

class SpeedTest(Test):
    def __init__(self, 
                 name: str, 
                 description: Optional[str] = None, 
                 protocol: Optional[TestProtocol] = None,
                 id: Optional[UUID] = None):
        super().__init__(
            name=name,
            category=TestCategory.SPEED,
            primary_unit=TestUnit.SECONDS,
            description=description,
            protocol=protocol,
            id=id
        )

class PowerTest(Test):
    def __init__(
        self, 
        name: str, 
        primary_unit: TestUnit,
        description: Optional[str] = None,
        protocol: Optional[TestProtocol] = None,
        additional_variables: List[AdditionalVariable] = None,
        id: Optional[UUID] = None
    ):
        super().__init__(
            name=name,
            category=TestCategory.POWER,
            primary_unit=primary_unit,
            description=description,
            protocol=protocol,
            additional_variables=additional_variables,
            id=id
        )

class TestResult(AggregateRoot):
    def __init__(
        self,
        athlete_id: UUID,
        test_id: UUID,
        value: float,
        test_date: datetime,
        phase: TestPhase,
        additional_values: Optional[Dict] = None,
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
    def athlete_id(self) -> UUID:
        return self._athlete_id

    @property
    def test_id(self) -> UUID:
        return self._test_id

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
    def additional_values(self) -> Dict:
        return self._additional_values.copy()