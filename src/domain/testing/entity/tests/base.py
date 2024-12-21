from dataclasses import dataclass
from typing import List, Optional, Dict
from uuid import UUID
from enum import Enum
from datetime import datetime
from ..value_objects import TestCategory, TestUnit, TestProtocol

class TestStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ARCHIVED = "Archived"

class TestFrequency(Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    AS_NEEDED = "As Needed"

@dataclass
class TestConfiguration:
    """Configuration for test execution and validation"""
    requires_equipment: bool = False
    equipment_list: List[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    decimal_places: int = 2
    multiple_trials: bool = False
    rest_period: Optional[int] = None  # in seconds
    requires_warmup: bool = False
    has_normative_data: bool = False

@dataclass
class TestVariable:
    """Represents a variable measured in a test"""
    name: str
    unit: TestUnit
    is_required: bool
    calculation_formula: Optional[str] = None
    dependent_variables: List[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None

class BaseTest:
    """Base class for all tests"""
    def __init__(
        self,
        name: str,
        category: TestCategory,
        primary_unit: TestUnit,
        description: Optional[str] = None,
        protocol: Optional[TestProtocol] = None,
        variables: List[TestVariable] = None,
        configuration: Optional[TestConfiguration] = None,
        id: Optional[UUID] = None
    ):
        self.id = id or uuid4()
        self.name = name
        self.category = category
        self.primary_unit = primary_unit
        self.description = description
        self.protocol = protocol
        self.variables = variables or []
        self.configuration = configuration or TestConfiguration()
        self.status = TestStatus.ACTIVE
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()

    def validate_result(self, value: float, variable_name: str = None) -> bool:
        """Validate a test result"""
        if variable_name:
            variable = next((v for v in self.variables if v.name == variable_name), None)
            if variable:
                return self._validate_value(value, variable.min_value, variable.max_value)
        return self._validate_value(
            value, 
            self.configuration.min_value, 
            self.configuration.max_value
        )

    def _validate_value(self, value: float, min_value: Optional[float], max_value: Optional[float]) -> bool:
        """Validate a value against min and max bounds"""
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True

    def calculate_derived_variables(self, primary_value: float, additional_values: Dict) -> Dict:
        """Calculate derived variables based on formulas"""
        results = {}
        for variable in self.variables:
            if variable.calculation_formula and variable.dependent_variables:
                if all(dep in additional_values for dep in variable.dependent_variables):
                    try:
                        # Here we'll implement safe formula evaluation
                        # This will be expanded when we implement the web interface
                        pass
                    except Exception as e:
                        # Log error and continue
                        pass
        return results