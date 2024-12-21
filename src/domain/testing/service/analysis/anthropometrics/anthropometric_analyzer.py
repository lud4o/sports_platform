from typing import Dict, Optional
from uuid import UUID
from datetime import date, datetime
from ..base.base_analyzer import BaseAnalyzer
from .body_composition_analyzer import BodyCompositionAnalyzer
from .maturation_analyzer import MaturationAnalyzer
from .metrics import AnthropometricMetrics, BodyCompositionMetrics, MaturationMetrics

class AnthropometricAnalyzer(BaseAnalyzer):
    def __init__(self, result_repository):
        super().__init__(result_repository)
        self._body_comp_analyzer = BodyCompositionAnalyzer(result_repository)
        self._maturation_analyzer = MaturationAnalyzer(result_repository)

    def analyze(self, athlete_id: UUID, metrics: AnthropometricMetrics) -> Dict:
        """Comprehensive anthropometric analysis"""
        analysis = {
            "basic_measurements": self._analyze_basic_measurements(metrics),
            "longitudinal_growth": self._analyze_growth_trends(athlete_id, metrics)
        }

        # Add body composition analysis if required measurements are available
        if hasattr(metrics, 'waist_circumference'):
            body_comp_metrics = BodyCompositionMetrics(
                waist_circumference=metrics.waist_circumference,
                neck_circumference=metrics.neck_circumference,
                hip_circumference=metrics.hip_circumference,
                height=metrics.height,
                weight=metrics.weight,
                gender=metrics.gender
            )
            analysis["body_composition"] = self._body_comp_analyzer.analyze(body_comp_metrics)

        # Add maturation analysis if age and seated height are available
        if hasattr(metrics, 'seated_height') and metrics.birth_date:
            age = self._calculate_age(metrics.birth_date)
            maturation_metrics = MaturationMetrics(
                height=metrics.height,
                seated_height=metrics.seated_height,
                weight=metrics.weight,
                age=age
            )
            analysis["maturation"] = self._maturation_analyzer.analyze(maturation_metrics)

        return analysis

    def _analyze_basic_measurements(self, metrics: AnthropometricMetrics) -> Dict:
        """Analyze basic anthropometric measurements"""
        return {
            "height": {
                "value": metrics.height,
                "unit": "cm"
            },
            "weight": {
                "value": metrics.weight,
                "unit": "kg"
            },
            "bmi": {
                "value": round(self._calculate_bmi(metrics.weight, metrics.height), 1),
                "unit": "kg/m²"
            },
            "standing_reach": {
                "value": metrics.standing_reach,
                "unit": "cm"
            } if metrics.standing_reach else None
        }

    def _analyze_growth_trends(self, athlete_id: UUID, metrics: AnthropometricMetrics) -> Dict:
        """Analyze growth trends from historical data"""
        historical_data = self.get_historical_results(
            athlete_id=athlete_id,
            test_names=["Height", "Weight"],
            limit=10
        )
        
        return {
            "height_trend": self.analyze_trend(
                [r['height'] for r in historical_data],
                [r['date'] for r in historical_data]
            ) if historical_data else None,
            "weight_trend": self.analyze_trend(
                [r['weight'] for r in historical_data],
                [r['date'] for r in historical_data]
            ) if historical_data else None
        }