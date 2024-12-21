from ..base.base_analyzer import BaseAnalyzer
from .metrics import MaturationMetrics, MaturationStatus

class MaturationAnalyzer(BaseAnalyzer):
    def analyze(self, metrics: MaturationMetrics) -> Dict:
        """Analyze maturation status using PHV calculation"""
        # Calculate leg length if not provided
        if metrics.leg_length is None:
            metrics.leg_length = metrics.height - metrics.seated_height

        phv_score = self.calculate_phv(metrics)
        maturation_status = self._determine_maturation_status(phv_score)
        
        return {
            "phv_score": round(phv_score, 2),
            "maturation_status": maturation_status.value,
            "training_considerations": self._get_training_considerations(maturation_status),
            "recommendations": self._generate_recommendations(maturation_status)
        }

    def calculate_phv(self, metrics: MaturationMetrics) -> float:
        """
        Calculate Peak Height Velocity score using Mirwald equation
        """
        sitting_height_ratio = (metrics.seated_height / metrics.height) * 100
        
        # Mirwald equation implementation
        phv = -9.236 + \
              (0.0002708 * (metrics.leg_length * sitting_height_ratio)) + \
              (-0.001663 * (metrics.age * metrics.leg_length)) + \
              (0.007216 * (metrics.age * sitting_height_ratio)) + \
              (0.02292 * (metrics.weight / metrics.height * 100))
        
        return phv

    def _determine_maturation_status(self, phv_score: float) -> MaturationStatus:
        """Determine maturation status based on PHV score"""
        if phv_score < -1:
            return MaturationStatus.PRE_PHV
        elif -1 <= phv_score <= 1:
            return MaturationStatus.DURING_PHV
        else:
            return MaturationStatus.POST_PHV