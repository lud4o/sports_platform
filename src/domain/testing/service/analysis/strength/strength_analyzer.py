from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum
from datetime import datetime
from uuid import UUID

class StrengthLevel(Enum):
    ELITE = "Elite"
    ADVANCED = "Advanced"
    INTERMEDIATE = "Intermediate"
    DEVELOPING = "Developing"

@dataclass
class IMTPResult:
    peak_force: float
    relative_peak_force: float
    rfd_50: float
    force_200ms: float
    test_date: datetime
    athlete_id: UUID

class IMTPAnalyzer:
    """Analyzer for Isometric Mid-thigh Pull test results"""
    
    PEAK_FORCE_THRESHOLDS = {
        "elite": 35,      # N/kg
        "advanced": 30,
        "intermediate": 25
    }
    
    RFD_50_THRESHOLDS = {
        "elite": 8000,    # N/s
        "advanced": 6000,
        "intermediate": 4000
    }
    
    FORCE_200MS_THRESHOLDS = {
        "elite": 2500,    # N
        "advanced": 2000,
        "intermediate": 1500
    }

    def analyze_result(self, result: IMTPResult) -> Dict:
        """
        Analyze IMTP test result and provide assessment
        """
        analysis = {
            "force_production": self._assess_force_production(result.peak_force, result.relative_peak_force),
            "explosive_strength": self._assess_explosive_strength(result.rfd_50),
            "early_force": self._assess_early_force(result.force_200ms),
            "training_recommendations": self._generate_recommendations(
                result.relative_peak_force,
                result.rfd_50,
                result.force_200ms
            )
        }
        
        return analysis

    def _assess_force_production(self, peak_force: float, relative_peak_force: float) -> Dict:
        level = self._assess_level(relative_peak_force, self.PEAK_FORCE_THRESHOLDS)
        return {
            "absolute_force": peak_force,
            "relative_force": relative_peak_force,
            "level": level.value,
            "score": self._calculate_score(relative_peak_force, self.PEAK_FORCE_THRESHOLDS)
        }

    def _assess_explosive_strength(self, rfd_50: float) -> Dict:
        level = self._assess_level(rfd_50, self.RFD_50_THRESHOLDS)
        return {
            "rfd_value": rfd_50,
            "level": level.value,
            "score": self._calculate_score(rfd_50, self.RFD_50_THRESHOLDS)
        }

    def _assess_early_force(self, force_200ms: float) -> Dict:
        level = self._assess_level(force_200ms, self.FORCE_200MS_THRESHOLDS)
        return {
            "force_value": force_200ms,
            "level": level.value,
            "score": self._calculate_score(force_200ms, self.FORCE_200MS_THRESHOLDS)
        }

    def _assess_level(self, value: float, thresholds: Dict[str, float]) -> StrengthLevel:
        if value >= thresholds["elite"]:
            return StrengthLevel.ELITE
        elif value >= thresholds["advanced"]:
            return StrengthLevel.ADVANCED
        elif value >= thresholds["intermediate"]:
            return StrengthLevel.INTERMEDIATE
        return StrengthLevel.DEVELOPING

    def _calculate_score(self, value: float, thresholds: Dict[str, float]) -> float:
        """Calculate a 0-100 score based on thresholds"""
        max_value = thresholds["elite"] * 1.2  # 20% above elite threshold
        return min(100, (value / max_value) * 100)

    def _generate_recommendations(self, relative_force: float, rfd_50: float, force_200ms: float) -> Dict:
        recommendations = {
            "focus_areas": [],
            "exercises": [],
            "training_parameters": {}
        }

        # Check force production
        if relative_force < self.PEAK_FORCE_THRESHOLDS["advanced"]:
            recommendations["focus_areas"].append("Maximum Strength Development")
            recommendations["exercises"].extend([
                "Back Squat (3-5 reps)",
                "Deadlift (3-5 reps)",
                "Push Press (3-5 reps)"
            ])
            recommendations["training_parameters"]["strength"] = {
                "intensity": "80-90% 1RM",
                "sets": "4-6",
                "reps": "3-5",
                "rest": "3-5 min"
            }

        # Check explosive strength
        if rfd_50 < self.RFD_50_THRESHOLDS["advanced"]:
            recommendations["focus_areas"].append("Explosive Strength Development")
            recommendations["exercises"].extend([
                "Power Clean",
                "Jump Squats",
                "Olympic Pull Variations"
            ])
            recommendations["training_parameters"]["power"] = {
                "intensity": "60-70% 1RM",
                "sets": "4-6",
                "reps": "3-5",
                "rest": "2-3 min"
            }

        return recommendations