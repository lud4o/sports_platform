# src/domain/testing/service/analysis/speed_acceleration_profiler.py
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from enum import Enum
import numpy as np

@dataclass
class AccelerationMetrics:
    value: float
    quality: str
    relative_score: float
    interpretation: str

class SpeedQuality(Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    AVERAGE = "Average"
    NEEDS_IMPROVEMENT = "Needs Improvement"

class SpeedAccelerationProfiler:
    # Constants for analysis
    ACCELERATION_THRESHOLDS = {
        "excellent": 5.5,  # m/s²
        "good": 4.5,
        "average": 3.5
    }
    
    MAX_SPEED_THRESHOLDS = {
        "excellent": 9.5,  # m/s
        "good": 8.5,
        "average": 7.5
    }

    def analyze_acceleration_profile(self, 
                                   sprint_10m: float, 
                                   sprint_20m: float,
                                   flying_10m: Optional[float] = None) -> Dict:
        """
        Comprehensive acceleration and speed analysis
        Args:
            sprint_10m: Time for 10m sprint (seconds)
            sprint_20m: Time for 20m sprint (seconds)
            flying_10m: Optional time for flying 10m (seconds)
        """
        profile = {
            "pure_acceleration": self._analyze_initial_acceleration(sprint_10m),
            "speed_endurance": self._analyze_speed_maintenance(sprint_10m, sprint_20m),
            "acceleration_curve": self._calculate_acceleration_curve(sprint_10m, sprint_20m)
        }
        
        if flying_10m:
            profile["max_speed"] = self._analyze_max_speed(flying_10m)
            profile["acceleration_deficit"] = self._calculate_acceleration_deficit(
                sprint_10m, flying_10m
            )

        return profile

    def _analyze_initial_acceleration(self, sprint_10m: float) -> Dict:
        """Analyze initial acceleration phase (0-10m)"""
        velocity = 10 / sprint_10m
        acceleration = (velocity ** 2) / (2 * 10)
        
        quality = self._evaluate_acceleration(acceleration)
        relative_score = self._calculate_relative_score(acceleration, self.ACCELERATION_THRESHOLDS)

        return {
            "metrics": AccelerationMetrics(
                value=round(acceleration, 2),
                quality=quality.value,
                relative_score=round(relative_score, 2),
                interpretation=self._get_acceleration_interpretation(quality)
            ),
            "velocity": round(velocity, 2),
            "time": sprint_10m
        }

    def _analyze_speed_maintenance(self, sprint_10m: float, sprint_20m: float) -> Dict:
        """Analyze speed maintenance phase (10-20m)"""
        second_10m = sprint_20m - sprint_10m
        initial_velocity = 10 / sprint_10m
        final_velocity = 10 / second_10m
        
        velocity_drop = ((initial_velocity - final_velocity) / initial_velocity) * 100
        maintenance_quality = self._evaluate_speed_maintenance(velocity_drop)

        return {
            "second_10m_time": round(second_10m, 2),
            "velocity_drop_percentage": round(velocity_drop, 2),
            "quality": maintenance_quality.value,
            "initial_velocity": round(initial_velocity, 2),
            "final_velocity": round(final_velocity, 2)
        }

    def _calculate_acceleration_curve(self, sprint_10m: float, sprint_20m: float) -> Dict:
        """Calculate detailed acceleration curve"""
        # Calculate velocities at different points
        v_10 = 10 / sprint_10m
        v_20 = 20 / sprint_20m
        
        # Calculate acceleration at different phases
        a_0_10 = (v_10 ** 2) / (2 * 10)
        a_10_20 = ((v_20 ** 2) - (v_10 ** 2)) / (2 * 10)
        
        # Calculate acceleration decrease
        acc_decrease = ((a_0_10 - a_10_20) / a_0_10) * 100

        return {
            "acceleration_phases": {
                "0-10m": round(a_0_10, 2),
                "10-20m": round(a_10_20, 2)
            },
            "acceleration_decrease": round(acc_decrease, 2),
            "curve_quality": self._evaluate_acceleration_curve(acc_decrease),
            "velocity_progression": {
                "10m": round(v_10, 2),
                "20m": round(v_20, 2)
            }
        }

    def _analyze_max_speed(self, flying_10m: float) -> Dict:
        """Analyze maximum speed capabilities"""
        max_velocity = 10 / flying_10m
        quality = self._evaluate_max_speed(max_velocity)
        relative_score = self._calculate_relative_score(max_velocity, self.MAX_SPEED_THRESHOLDS)

        return {
            "max_velocity": round(max_velocity, 2),
            "quality": quality.value,
            "relative_score": round(relative_score, 2),
            "time": flying_10m
        }

    def _calculate_acceleration_deficit(self, sprint_10m: float, flying_10m: float) -> Dict:
        """Calculate acceleration deficit comparing max speed to acceleration ability"""
        acceleration_velocity = 10 / sprint_10m
        max_velocity = 10 / flying_10m
        
        deficit = ((max_velocity - acceleration_velocity) / max_velocity) * 100
        deficit_quality = self._evaluate_acceleration_deficit(deficit)

        return {
            "deficit_percentage": round(deficit, 2),
            "quality": deficit_quality.value,
            "interpretation": self._get_deficit_interpretation(deficit_quality),
            "acceleration_velocity": round(acceleration_velocity, 2),
            "max_velocity": round(max_velocity, 2)
        }

    def _evaluate_acceleration(self, acceleration: float) -> SpeedQuality:
        """Evaluate acceleration quality"""
        if acceleration >= self.ACCELERATION_THRESHOLDS["excellent"]:
            return SpeedQuality.EXCELLENT
        elif acceleration >= self.ACCELERATION_THRESHOLDS["good"]:
            return SpeedQuality.GOOD
        elif acceleration >= self.ACCELERATION_THRESHOLDS["average"]:
            return SpeedQuality.AVERAGE
        return SpeedQuality.NEEDS_IMPROVEMENT

    def _evaluate_speed_maintenance(self, velocity_drop: float) -> SpeedQuality:
        """Evaluate speed maintenance quality"""
        if velocity_drop <= 5:
            return SpeedQuality.EXCELLENT
        elif velocity_drop <= 10:
            return SpeedQuality.GOOD
        elif velocity_drop <= 15:
            return SpeedQuality.AVERAGE
        return SpeedQuality.NEEDS_IMPROVEMENT

    def _evaluate_max_speed(self, velocity: float) -> SpeedQuality:
        """Evaluate maximum speed quality"""
        if velocity >= self.MAX_SPEED_THRESHOLDS["excellent"]:
            return SpeedQuality.EXCELLENT
        elif velocity >= self.MAX_SPEED_THRESHOLDS["good"]:
            return SpeedQuality.GOOD
        elif velocity >= self.MAX_SPEED_THRESHOLDS["average"]:
            return SpeedQuality.AVERAGE
        return SpeedQuality.NEEDS_IMPROVEMENT

    def _evaluate_acceleration_deficit(self, deficit: float) -> SpeedQuality:
        """Evaluate acceleration deficit quality"""
        if deficit <= 15:
            return SpeedQuality.EXCELLENT
        elif deficit <= 20:
            return SpeedQuality.GOOD
        elif deficit <= 25:
            return SpeedQuality.AVERAGE
        return SpeedQuality.NEEDS_IMPROVEMENT

    def _calculate_relative_score(self, value: float, thresholds: Dict[str, float]) -> float:
        """Calculate relative score (0-100) based on thresholds"""
        if value >= thresholds["excellent"]:
            return 100
        elif value >= thresholds["good"]:
            return 75 + (value - thresholds["good"]) / (thresholds["excellent"] - thresholds["good"]) * 25
        elif value >= thresholds["average"]:
            return 50 + (value - thresholds["average"]) / (thresholds["good"] - thresholds["average"]) * 25
        return max(0, (value / thresholds["average"]) * 50)

    def _get_acceleration_interpretation(self, quality: SpeedQuality) -> str:
        """Get interpretation text based on acceleration quality"""
        interpretations = {
            SpeedQuality.EXCELLENT: "Elite level acceleration capability, focus on maintaining this quality",
            SpeedQuality.GOOD: "Strong acceleration ability, minor improvements possible through targeted training",
            SpeedQuality.AVERAGE: "Typical acceleration profile, potential for improvement through power development",
            SpeedQuality.NEEDS_IMPROVEMENT: "Focus required on explosive strength and acceleration technique"
        }
        return interpretations.get(quality, "")

    def _get_deficit_interpretation(self, quality: SpeedQuality) -> str:
        """Get interpretation text based on deficit quality"""
        interpretations = {
            SpeedQuality.EXCELLENT: "Excellent balance between acceleration and max speed",
            SpeedQuality.GOOD: "Good acceleration-speed relationship, minor optimization possible",
            SpeedQuality.AVERAGE: "Typical acceleration-speed relationship, room for improvement",
            SpeedQuality.NEEDS_IMPROVEMENT: "Significant imbalance between acceleration and max speed"
        }
        return interpretations.get(quality, "")