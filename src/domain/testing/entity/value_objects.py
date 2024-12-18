from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
from domain.core.value_object import ValueObject

class TestCategory(Enum):
    SPEED = "Speed"
    POWER = "Power"
    STRENGTH = "Strength"
    ENDURANCE = "Endurance"
    FLEXIBILITY = "Flexibility"
    ANTHROPOMETRICS = "Anthropometrics"

class TestUnit(Enum):
    SECONDS = "sec"
    CENTIMETERS = "cm"
    KILOGRAMS = "kg"
    METERS_PER_SECOND = "m/s"
    LEVEL = "level"  # For beep test
    KILOMETERS = "km"
    NEWTONS = "N"
    REPETITIONS = "reps"
    NEWTONS_PER_SECOND = "N/s"
    NEWTONS_PER_KILOGRAM = "N/kg"

class AnalysisType(Enum):
    SINGLE = "Single Test Analysis"
    COMPARATIVE = "Comparative Analysis"
    TREND = "Trend Analysis"
    RATIO = "Ratio Analysis"

@dataclass(frozen=True)
class TestProtocol(ValueObject):
    name: str
    description: str
    setup_instructions: Optional[str] = None
    measurement_guidelines: Optional[str] = None
    required_equipment: Optional[List[str]] = None

@dataclass(frozen=True)
class AdditionalVariable:
    name: str
    unit: TestUnit
    is_required: bool = False
    calculation_formula: Optional[str] = None  # For derived measurements
    dependent_variables: Optional[List[str]] = None  # Variables needed for calculation