from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime
from uuid import UUID
import numpy as np
from scipy import stats

class BaseAnalyzer(ABC):
    """Base class for all performance analyzers"""

    def __init__(self, result_repository):
        self._result_repository = result_repository

    @abstractmethod
    def analyze(self, *args, **kwargs) -> Dict[str, Any]:
        """Main analysis method to be implemented by specific analyzers"""
        pass

    def get_historical_results(self, 
                             athlete_id: UUID,
                             test_names: List[str],
                             time_period: Optional[tuple] = None,
                             limit: int = 10) -> List[Dict]:
        """Fetch historical test results"""
        return self._result_repository.get_historical_results(
            athlete_id=athlete_id,
            test_names=test_names,
            time_period=time_period,
            limit=limit
        )

    def calculate_basic_statistics(self, values: List[float]) -> Dict[str, float]:
        """Calculate basic statistical measures"""
        if not values:
            return {}

        return {
            "mean": float(np.mean(values)),
            "std": float(np.std(values)),
            "min": float(np.min(values)),
            "max": float(np.max(values)),
            "latest": values[-1],
            "trend": self._calculate_trend(values)
        }

    def calculate_percentile_rank(self, 
                                value: float, 
                                reference_values: List[float]) -> float:
        """Calculate percentile rank of a value within a reference group"""
        if not reference_values:
            return 0.0
        return stats.percentileofscore(reference_values, value)

    def analyze_trend(self, 
                     values: List[float], 
                     dates: List[datetime]) -> Dict[str, Any]:
        """Analyze performance trend over time"""
        if len(values) < 2:
            return {"trend": "insufficient_data"}

        x = np.array([(date - dates[0]).days for date in dates])
        y = np.array(values)
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        return {
            "slope": float(slope),
            "r_squared": float(r_value**2),
            "significance": float(p_value),
            "direction": "improving" if slope > 0 else "declining",
            "confidence": self._calculate_confidence_band(x, y, slope, intercept)
        }

    def _calculate_trend(self, values: List[float], window: int = 3) -> str:
        """Calculate recent trend direction"""
        if len(values) < window:
            return "insufficient_data"
            
        recent = values[-window:]
        slope = np.polyfit(range(len(recent)), recent, 1)[0]
        
        if abs(slope) < 0.01:  # Threshold for stability
            return "stable"
        return "improving" if slope > 0 else "declining"

    def _calculate_confidence_band(self, 
                                 x: np.ndarray, 
                                 y: np.ndarray, 
                                 slope: float, 
                                 intercept: float,
                                 confidence: float = 0.95) -> Dict[str, List[float]]:
        """Calculate confidence bands for trend line"""
        n = len(x)
        if n < 3:
            return {"upper": [], "lower": []}

        # Fit values
        y_fit = slope * x + intercept
        
        # Sum of squares
        s_err = np.sqrt(np.sum((y - y_fit) ** 2) / (n - 2))
        
        # Critical value
        t_val = stats.t.ppf((1 + confidence) / 2, n - 2)
        
        # Confidence bands
        confs = t_val * s_err * np.sqrt(1/n + (x - np.mean(x))**2 / np.sum((x - np.mean(x))**2))
        
        return {
            "upper": (y_fit + confs).tolist(),
            "lower": (y_fit - confs).tolist()
        }

    def generate_summary(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate human-readable summary from analysis metrics"""
        summary = []
        
        # Add key findings based on metrics
        if "trend" in metrics:
            summary.append(f"Performance trend is {metrics['trend']}")
            
        if "percentile" in metrics:
            summary.append(f"Current performance is in the {metrics['percentile']:.1f}th percentile")
            
        return summary