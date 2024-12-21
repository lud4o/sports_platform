from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime
from ..base.base_analyzer import BaseAnalyzer
from .strength_metrics import StrengthMetricsCalculator, IMTPMetrics, StrengthLevel

class IMTPAnalyzer(BaseAnalyzer):
    """Analyzer for Isometric Mid-thigh Pull test results"""
    
    def __init__(self, result_repository):
        super().__init__(result_repository)
        self._metrics_calculator = StrengthMetricsCalculator()

    def analyze(self, 
                athlete_id: UUID,
                peak_force: float,
                rfd_50: float,
                force_200ms: float,
                body_mass: float,
                test_date: Optional[datetime] = None) -> Dict:
        """Main analysis method implementing BaseAnalyzer.analyze"""
        if test_date is None:
            test_date = datetime.now()

        result = IMTPMetrics(
            peak_force=peak_force,
            relative_peak_force=peak_force / body_mass,
            rfd_50=rfd_50,
            force_200ms=force_200ms,
            test_date=test_date,
            athlete_id=athlete_id
        )

        analysis = self.analyze_result(result)

        # Add historical analysis
        historical = self.get_historical_results(
            athlete_id=athlete_id,
            test_names=["IMTP"],
            limit=10
        )

        if historical:
            analysis["trends"] = self.analyze_trend(
                [r['peak_force'] for r in historical],
                [r['date'] for r in historical]
            )

        return analysis

    def analyze_result(self, result: IMTPMetrics) -> Dict:
        """Analyze IMTP test result and provide assessment"""
        thresholds = self._metrics_calculator.IMTP_THRESHOLDS
        
        analysis = {
            "force_production": self._assess_force_production(
                result.peak_force, 
                result.relative_peak_force
            ),
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
        """Assess force production capabilities"""
        level = self._metrics_calculator.assess_strength_level(
            relative_peak_force, 
            self._metrics_calculator.IMTP_THRESHOLDS["peak_force"]
        )
        return {
            "absolute_force": peak_force,
            "relative_force": relative_peak_force,
            "level": level.value,
            "score": self._metrics_calculator.calculate_score(
                relative_peak_force,
                self._metrics_calculator.IMTP_THRESHOLDS["peak_force"]
            )
        }
    
    def _assess_explosive_strength(self, rfd_50: float) -> Dict:
        """Assess rate of force development capabilities"""
        level = self._metrics_calculator.assess_strength_level(
            rfd_50, 
            self._metrics_calculator.IMTP_THRESHOLDS["rfd_50"]
        )
        
        return {
            "rfd_value": rfd_50,
            "level": level.value,
            "score": self._metrics_calculator.calculate_score(
                rfd_50,
                self._metrics_calculator.IMTP_THRESHOLDS["rfd_50"]
            ),
            "interpretation": self._get_rfd_interpretation(level)
        }

    def _assess_early_force(self, force_200ms: float) -> Dict:
        """Assess early force production capabilities"""
        level = self._metrics_calculator.assess_strength_level(
            force_200ms, 
            self._metrics_calculator.IMTP_THRESHOLDS["force_200ms"]
        )
        
        return {
            "force_value": force_200ms,
            "level": level.value,
            "score": self._metrics_calculator.calculate_score(
                force_200ms,
                self._metrics_calculator.IMTP_THRESHOLDS["force_200ms"]
            ),
            "interpretation": self._get_early_force_interpretation(level)
        }

    def _generate_recommendations(self, relative_force: float, rfd_50: float, force_200ms: float) -> Dict:
        """Generate specific training recommendations based on assessment"""
        recommendations = {
            "focus_areas": [],
            "exercises": [],
            "training_parameters": {},
            "priorities": self._determine_training_priorities(relative_force, rfd_50, force_200ms)
        }

        # Check force production
        if relative_force < self._metrics_calculator.IMTP_THRESHOLDS["peak_force"]["advanced"]:
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
                "rest": "3-5 min",
                "frequency": "2-3 times per week",
                "progression": "Increase load when all sets are completed with good form"
            }

        # Check explosive strength
        if rfd_50 < self._metrics_calculator.IMTP_THRESHOLDS["rfd_50"]["advanced"]:
            recommendations["focus_areas"].append("Explosive Strength Development")
            recommendations["exercises"].extend([
                "Power Clean",
                "Jump Squats",
                "Olympic Pull Variations",
                "Plyometric Combinations"
            ])
            recommendations["training_parameters"]["power"] = {
                "intensity": "60-70% 1RM",
                "sets": "4-6",
                "reps": "3-5",
                "rest": "2-3 min",
                "frequency": "2-3 times per week",
                "progression": "Focus on movement velocity and technical execution"
            }

        # Check early force production
        if force_200ms < self._metrics_calculator.IMTP_THRESHOLDS["force_200ms"]["advanced"]:
            recommendations["focus_areas"].append("Early Force Production")
            recommendations["exercises"].extend([
                "Speed-Strength Exercises",
                "Ballistic Exercises",
                "Heavy Isometric Pulls"
            ])
            recommendations["training_parameters"]["early_force"] = {
                "intensity": "varies by exercise",
                "sets": "3-5",
                "reps": "3-6",
                "rest": "2-3 min",
                "frequency": "2 times per week",
                "emphasis": "Explosive intent in each repetition"
            }

        return recommendations

    def _determine_training_priorities(self, relative_force: float, rfd_50: float, force_200ms: float) -> List[str]:
        """Determine training priorities based on assessments"""
        priorities = []
        
        # Calculate percentage from threshold for each metric
        force_percent = (relative_force / self._metrics_calculator.IMTP_THRESHOLDS["peak_force"]["advanced"]) * 100
        rfd_percent = (rfd_50 / self._metrics_calculator.IMTP_THRESHOLDS["rfd_50"]["advanced"]) * 100
        early_force_percent = (force_200ms / self._metrics_calculator.IMTP_THRESHOLDS["force_200ms"]["advanced"]) * 100
        
        # Sort metrics by percentage from threshold
        metrics = [
            ("Maximum Strength", force_percent),
            ("Rate of Force Development", rfd_percent),
            ("Early Force Production", early_force_percent)
        ]
        
        # Sort by percentage (lowest first - highest priority)
        sorted_metrics = sorted(metrics, key=lambda x: x[1])
        return [metric[0] for metric in sorted_metrics]

    def _get_rfd_interpretation(self, level: StrengthLevel) -> str:
        """Get interpretation text for RFD level"""
        interpretations = {
            StrengthLevel.ELITE: "Elite explosive strength capability, focus on maintenance",
            StrengthLevel.ADVANCED: "Strong explosive strength, minor refinements needed",
            StrengthLevel.INTERMEDIATE: "Moderate explosive strength, focus on specific RFD training",
            StrengthLevel.DEVELOPING: "Requires focused development of explosive strength"
        }
        return interpretations.get(level, "")

    def _get_early_force_interpretation(self, level: StrengthLevel) -> str:
        """Get interpretation text for early force production level"""
        interpretations = {
            StrengthLevel.ELITE: "Excellent early force production, maintain current capability",
            StrengthLevel.ADVANCED: "Good early force development, minor improvements possible",
            StrengthLevel.INTERMEDIATE: "Average early force production, room for improvement",
            StrengthLevel.DEVELOPING: "Focus needed on early force production development"
        }
        return interpretations.get(level, "")

    def analyze_bilateral_ratio(self, left_peak_force: float, right_peak_force: float) -> Dict:
        """Analyze bilateral force production ratio"""
        stronger_side = max(left_peak_force, right_peak_force)
        weaker_side = min(left_peak_force, right_peak_force)
        asymmetry = ((stronger_side - weaker_side) / stronger_side) * 100
        
        return {
            "stronger_side": "left" if left_peak_force > right_peak_force else "right",
            "asymmetry_percent": round(asymmetry, 2),
            "ratio": round(weaker_side / stronger_side, 2),
            "assessment": self._assess_asymmetry(asymmetry)
        }

    def _assess_asymmetry(self, asymmetry: float) -> str:
        """Assess the significance of force production asymmetry"""
        if asymmetry <= 5:
            return "normal"
        elif asymmetry <= 10:
            return "minor"
        elif asymmetry <= 15:
            return "moderate"
        return "significant"