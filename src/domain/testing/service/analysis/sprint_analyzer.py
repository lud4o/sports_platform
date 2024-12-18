from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from uuid import UUID
from enum import Enum
from .speed_acceleration_profiler import SpeedAccelerationProfiler, SpeedQuality

class TrainingFocus(Enum):
    STRENGTH = "Strength Program"
    POWER = "Power Program"
    SPEED = "Speed/Strength Program"

@dataclass
class TrainingRecommendation:
    focus: str
    key_exercises: List[str]
    training_emphasis: str
    volume: str
    rest: str
    progression_notes: str

@dataclass
class SprintResults:
    sprint_10m: float
    sprint_20m: float
    flying_10m: Optional[float] = None
    historical_results: Optional[List[Dict]] = None

class SprintAnalyzer:
    def __init__(self, result_repository):
        self._result_repository = result_repository
        self._speed_profiler = SpeedAccelerationProfiler()

    def analyze_sprint_profile(self, athlete_id: UUID, test_date: datetime) -> Dict:
        """Complete sprint profile analysis"""
        sprint_results = self._get_sprint_results(athlete_id, test_date)
        
        if not sprint_results:
            raise ValueError("No sprint results found for specified date")

        basic_analysis = self._analyze_sprint_metrics(
            sprint_results.sprint_10m, 
            sprint_results.sprint_20m,
            sprint_results.flying_10m
        )

        # Get historical results for trend analysis
        if sprint_results.historical_results:
            basic_analysis["trends"] = self._analyze_trends(sprint_results.historical_results)

        return basic_analysis

    def _get_sprint_results(self, athlete_id: UUID, test_date: datetime) -> SprintResults:
        """Fetch all relevant sprint results"""
        sprint_10m = self._result_repository.get_latest_result(
            athlete_id=athlete_id,
            test_name="10M Sprint",
            date=test_date
        )
        sprint_20m = self._result_repository.get_latest_result(
            athlete_id=athlete_id,
            test_name="20M Sprint",
            date=test_date
        )
        flying_10m = self._result_repository.get_latest_result(
            athlete_id=athlete_id,
            test_name="Flying 10M",
            date=test_date
        )

        if not sprint_10m or not sprint_20m:
            raise ValueError("Both 10m and 20m sprint results required")

        # Get historical results for trend analysis
        historical = self._result_repository.get_historical_results(
            athlete_id=athlete_id,
            test_names=["10M Sprint", "20M Sprint", "Flying 10M"],
            limit=10
        )

        return SprintResults(
            sprint_10m=sprint_10m.value,
            sprint_20m=sprint_20m.value,
            flying_10m=flying_10m.value if flying_10m else None,
            historical_results=historical
        )

    def _analyze_sprint_metrics(self, 
                              sprint_10m: float, 
                              sprint_20m: float,
                              flying_10m: Optional[float] = None) -> Dict:
        """Comprehensive sprint analysis"""
        # Get acceleration profile
        acceleration_profile = self._speed_profiler.analyze_acceleration_profile(
            sprint_10m, sprint_20m, flying_10m
        )

        # Calculate normalized 20m score for training recommendations
        normalized_20m = sprint_20m * (1.0 / sprint_10m)
        program, recommendations = self._get_training_recommendations(
            normalized_20m,
            acceleration_profile
        )

        return {
            "sprint_times": {
                "10m": sprint_10m,
                "20m": sprint_20m,
                "flying_10m": flying_10m
            },
            "acceleration_profile": acceleration_profile,
            "training_program": program,
            "recommendations": recommendations,
            "performance_summary": self._generate_performance_summary(
                acceleration_profile, flying_10m
            )
        }

    def _get_training_recommendations(self, 
                                    normalized_20m: float,
                                    acceleration_profile: Dict) -> Tuple[str, TrainingRecommendation]:
        """Generate specific training recommendations"""
        # Analyze acceleration qualities
        initial_acc_quality = acceleration_profile["pure_acceleration"]["metrics"].quality
        speed_maint_quality = acceleration_profile["speed_endurance"]["quality"]

        if normalized_20m <= 1.79:
            return (
                TrainingFocus.STRENGTH.value,
                TrainingRecommendation(
                    focus="Acceleration and Force Production",
                    key_exercises=[
                        "Heavy Squats (3-5 reps)",
                        "Deadlifts (3-5 reps)",
                        "Power Cleans (3-5 reps)",
                        "Weighted Jumps",
                        "Hill Sprints"
                    ],
                    training_emphasis="Focus on maximal strength and explosive power",
                    volume="3-4 sets per exercise, 2-3 times per week",
                    rest="2-3 minutes between sets",
                    progression_notes="Increase weight when 3x5 is achieved with good form"
                )
            )
        elif 1.79 < normalized_20m <= 1.82:
            return (
                TrainingFocus.POWER.value,
                TrainingRecommendation(
                    focus="Speed-Strength Development",
                    key_exercises=[
                        "Jump Squats",
                        "Trap Bar Jumps",
                        "Olympic Lifts",
                        "Resisted Sprints",
                        "Plyometric Combinations"
                    ],
                    training_emphasis="Focus on explosive power and rate of force development",
                    volume="4-6 sets per exercise, 2-3 times per week",
                    rest="2 minutes between sets",
                    progression_notes="Progress by increasing movement velocity"
                )
            )
        else:
            return (
                TrainingFocus.SPEED.value,
                TrainingRecommendation(
                    focus="Speed and Technique",
                    key_exercises=[
                        "Sprint Technique Drills",
                        "Flying Sprints",
                        "Rolling Starts",
                        "Sprint Bounds",
                        "Light Plyometrics"
                    ],
                    training_emphasis="Focus on sprint mechanics and neural activation",
                    volume="5-8 sets per exercise, 2-3 times per week",
                    rest="Full recovery (2-3 minutes)",
                    progression_notes="Focus on quality and technical execution"
                )
            )

    def _generate_performance_summary(self, 
                                    acceleration_profile: Dict,
                                    flying_10m: Optional[float]) -> Dict:
        """Generate overall performance summary"""
        summary = {
            "acceleration_ability": acceleration_profile["pure_acceleration"]["metrics"].quality,
            "speed_maintenance": acceleration_profile["speed_endurance"]["quality"],
            "key_findings": [],
            "primary_focus": []
        }

        # Add findings based on acceleration profile
        if acceleration_profile["pure_acceleration"]["metrics"].quality == SpeedQuality.NEEDS_IMPROVEMENT:
            summary["key_findings"].append("Initial acceleration needs significant improvement")
            summary["primary_focus"].append("Force production and starting strength")

        if acceleration_profile["speed_endurance"]["quality"] == SpeedQuality.NEEDS_IMPROVEMENT:
            summary["key_findings"].append("Speed maintenance shows significant drop-off")
            summary["primary_focus"].append("Speed endurance and technical efficiency")

        if flying_10m:
            max_speed_quality = acceleration_profile["max_speed"]["quality"]
            summary["max_speed_ability"] = max_speed_quality
            
            if max_speed_quality == SpeedQuality.NEEDS_IMPROVEMENT:
                summary["key_findings"].append("Maximum speed capability needs development")
                summary["primary_focus"].append("Maximum velocity mechanics and power output")

        return summary

    def _analyze_trends(self, historical_results: List[Dict]) -> Dict:
        """Analyze performance trends over time"""
        # Implementation of trend analysis
        pass