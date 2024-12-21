from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

class StrengthLevel(Enum):
    ELITE = "Elite"
    ADVANCED = "Advanced"
    INTERMEDIATE = "Intermediate"
    DEVELOPING = "Developing"

@dataclass
class StrengthMetrics:
    absolute_value: float
    relative_value: float
    level: StrengthLevel
    score: float
    imbalance: Optional[float] = None

@dataclass
class IMTPMetrics:
    peak_force: float
    relative_peak_force: float
    rfd_50: float
    force_200ms: float
    test_date: datetime
    athlete_id: UUID

class StrengthMetricsCalculator:
    # Your existing IMTP thresholds
    IMTP_THRESHOLDS = {
        "peak_force": {
            "elite": 35,      # N/kg
            "advanced": 30,
            "intermediate": 25
        },
        "rfd_50": {
            "elite": 8000,    # N/s
            "advanced": 6000,
            "intermediate": 4000
        },
        "force_200ms": {
            "elite": 2500,    # N
            "advanced": 2000,
            "intermediate": 1500
        }
    }

    def calculate_relative_strength(self, absolute_value: float, body_mass: float) -> float:
        """Calculate relative strength"""
        return absolute_value / body_mass if body_mass > 0 else 0

    def assess_strength_level(self, value: float, thresholds: Dict) -> StrengthLevel:
        """Assess strength level based on thresholds"""
        if value >= thresholds["elite"]:
            return StrengthLevel.ELITE
        elif value >= thresholds["advanced"]:
            return StrengthLevel.ADVANCED
        elif value >= thresholds["intermediate"]:
            return StrengthLevel.INTERMEDIATE
        return StrengthLevel.DEVELOPING

    def calculate_score(self, value: float, thresholds: Dict[str, float]) -> float:
        """Calculate 0-100 score based on thresholds"""
        max_value = thresholds["elite"] * 1.2
        return min(100, (value / max_value) * 100)