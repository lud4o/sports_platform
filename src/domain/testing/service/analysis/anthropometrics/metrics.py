from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import date

class MaturationStatus(Enum):
    PRE_PHV = "Pre-PHV"
    DURING_PHV = "During PHV"
    POST_PHV = "Post-PHV"

@dataclass
class AnthropometricMetrics:
    height: float
    weight: float
    standing_reach: Optional[float] = None
    birth_date: Optional[date] = None
    leg_length_lying: Optional[float] = None
    leg_length_squat: Optional[float] = None

@dataclass
class BodyCompositionMetrics:
    waist_circumference: float
    neck_circumference: float
    hip_circumference: Optional[float] = None  # Required for females
    height: float
    weight: float
    gender: str

@dataclass
class MaturationMetrics:
    height: float
    seated_height: float
    weight: float
    age: float
    leg_length: float = None  # Calculated from height - seated_height