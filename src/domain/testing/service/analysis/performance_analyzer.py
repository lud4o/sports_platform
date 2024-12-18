from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from uuid import UUID
import numpy as np
from scipy import stats

@dataclass
class PerformanceMetrics:
    current_value: float
    personal_best: float
    improvement_rate: float
    percentile_rank: float
    relative_to_benchmark: float
    trend_direction: str
    confidence_interval: tuple

@dataclass
class TrendAnalysis:
    slope: float
    r_squared: float
    prediction_next: float
    confidence_band: tuple

class PerformanceAnalyzer:
    def __init__(self, test_repository, result_repository):
        self._test_repository = test_repository
        self._result_repository = result_repository

    def analyze_athlete_performance(self, 
                                  athlete_id: UUID,
                                  test_id: UUID,
                                  time_period: Optional[tuple] = None) -> PerformanceMetrics:
        """Analyze athlete's performance in a specific test"""
        results = self._result_repository.get_athlete_results(
            athlete_id=athlete_id,
            test_id=test_id,
            time_period=time_period
        )
        
        if not results:
            return None

        values = [r.value for r in results]
        dates = [r.test_date for r in results]

        return PerformanceMetrics(
            current_value=values[-1],
            personal_best=max(values) if test.higher_is_better else min(values),
            improvement_rate=self._calculate_improvement_rate(values),
            percentile_rank=self._calculate_percentile_rank(values[-1], test_id),
            relative_to_benchmark=self._calculate_benchmark_comparison(values[-1], test_id),
            trend_direction=self._analyze_trend(values),
            confidence_interval=self._calculate_confidence_interval(values)
        )

    def analyze_trend(self, 
                     values: List[float], 
                     dates: List[datetime]) -> TrendAnalysis:
        """Analyze performance trend over time"""
        x = np.array([(date - dates[0]).days for date in dates])
        y = np.array(values)
        
        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Predict next value
        next_x = x[-1] + 30  # Predict 30 days ahead
        prediction = slope * next_x + intercept
        
        # Calculate confidence band
        confidence_band = self._calculate_confidence_band(x, y, slope, intercept)
        
        return TrendAnalysis(
            slope=slope,
            r_squared=r_value**2,
            prediction_next=prediction,
            confidence_band=confidence_band
        )

    def _calculate_confidence_band(self, x, y, slope, intercept):
        """Calculate 95% confidence interval for trend line"""
        # Implementation of confidence band calculation
        pass