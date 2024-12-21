from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
from domain.core.value_object import ValueObject

class TestCategory(Enum):
    SPEED = "Speed"
    POWER = "Power"
    STRENGTH = "Strength"
    ANTHROPOMETRICS = "Anthropometrics"
    ENDURANCE = "Endurance"
    FLEXIBILITY = "Flexibility"
    AGILITY = "Agility"
    COORDINATION = "Coordination"

class TestUnit(Enum):
    # Time units
    SECONDS = "sec"
    MILLISECONDS = "ms"
    
    # Distance units
    CENTIMETERS = "cm"
    METERS = "m"
    KILOMETERS = "km"
    
    # Mass/Force units
    KILOGRAMS = "kg"
    NEWTONS = "N"
    NEWTONS_PER_SECOND = "N/s"
    NEWTONS_PER_KILOGRAM = "N/kg"
    
    # Speed units
    METERS_PER_SECOND = "m/s"
    KILOMETERS_PER_HOUR = "km/h"
    
    # Other measurement units
    LEVEL = "level"
    PERCENTAGE = "%"
    SCORE = "score"
    WATTS = "W"
    WATTS_PER_KILOGRAM = "W/kg"
    REPETITIONS = "reps"
    DEGREES = "°"

class TestEnvironment(Enum):
    INDOOR = "Indoor"
    OUTDOOR = "Outdoor"
    BOTH = "Both"

@dataclass(frozen=True)
class TestProtocol(ValueObject):
    name: str
    description: str
    setup_instructions: Optional[str] = None
    measurement_guidelines: Optional[str] = None
    safety_guidelines: Optional[str] = None
    required_equipment: List[str] = None
    environment: TestEnvironment = TestEnvironment.BOTH
    warmup_protocol: Optional[str] = None

@dataclass(frozen=True)
class AdditionalVariable:
    name: str
    unit: TestUnit
    is_required: bool = False
    calculation_formula: Optional[str] = None
    dependent_variables: Optional[List[str]] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    normative_data: Optional[dict] = None