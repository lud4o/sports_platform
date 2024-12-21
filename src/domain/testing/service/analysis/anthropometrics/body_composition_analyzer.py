from ..base.base_analyzer import BaseAnalyzer
from .metrics import BodyCompositionMetrics
import numpy as np

class BodyCompositionAnalyzer(BaseAnalyzer):
    def analyze(self, metrics: BodyCompositionMetrics) -> Dict:
        """Analyze body composition measurements"""
        body_fat = self.calculate_body_fat(
            gender=metrics.gender,
            waist_circ=metrics.waist_circumference,
            neck_circ=metrics.neck_circumference,
            height=metrics.height,
            hip_circ=metrics.hip_circumference
        )

        bmi = self.calculate_bmi(metrics.weight, metrics.height)
        
        return {
            "body_fat_percentage": round(body_fat, 1),
            "bmi": round(bmi, 1),
            "classification": self._classify_body_composition(body_fat, bmi, metrics.gender),
            "recommendations": self._generate_recommendations(body_fat, bmi)
        }

    def calculate_body_fat(self,
                         gender: str,
                         waist_circ: float,
                         neck_circ: float,
                         height: float,
                         hip_circ: Optional[float] = None) -> float:
        """Calculate body fat percentage using Navy method"""
        if gender.lower() == 'male':
            return 495 / (1.0324 - 0.19077 * np.log10(waist_circ - neck_circ) + 
                         0.15456 * np.log10(height)) - 450
        else:
            if hip_circ is None:
                raise ValueError("Hip circumference required for female calculation")
            return 495 / (1.29579 - 0.35004 * np.log10(waist_circ + hip_circ - neck_circ) +
                         0.22100 * np.log10(height)) - 450

    def calculate_bmi(self, weight: float, height: float) -> float:
        """Calculate BMI (height in cm, weight in kg)"""
        height_m = height / 100  # Convert cm to m
        return weight / (height_m * height_m)