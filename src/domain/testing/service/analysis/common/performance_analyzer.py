from typing import Dict, List, Optional, Union
from datetime import datetime
from uuid import UUID
import numpy as np
from scipy import stats
from ..base.base_analyzer import BaseAnalyzer
from .metrics import PerformanceMetrics, TrendAnalysis, TrendDirection

class PerformanceAnalyzer(BaseAnalyzer):
    def analyze(self, 
               athlete_id: UUID,
               test_id: UUID,
               time_period: Optional[tuple] = None) -> Dict:
        """Comprehensive performance analysis including trends"""
        # Get performance data
        results = self._result_repository.get_athlete_results(
            athlete_id=athlete_id,
            test_id=test_id,
            time_period=time_period
        )
        
        if not results:
            return None

        values = [r.value for r in results]
        dates = [r.test_date for r in results]

        # Basic performance metrics
        performance_metrics = self._analyze_performance(values, dates)
        
        # Trend analysis
        trend_analysis = self._analyze_trends(values, dates)
        
        return {
            "current_performance": performance_metrics,
            "trend_analysis": trend_analysis,
            "predictions": self._generate_predictions(values, dates),
            "recommendations": self._generate_recommendations(
                performance_metrics, 
                trend_analysis
            )
        }

    def _analyze_performance(self, values: List[float], dates: List[datetime]) -> PerformanceMetrics:
        """Analyze current performance status"""
        trend_analysis = self.analyze_trend(values, dates)
        
        return PerformanceMetrics(
            current_value=values[-1],
            personal_best=max(values),
            improvement_rate=self._calculate_improvement_rate(values),
            percentile_rank=self._calculate_percentile_rank(values[-1]),
            relative_to_benchmark=self._calculate_benchmark_comparison(values[-1]),
            trend_direction=self._determine_trend_direction(trend_analysis),
            confidence_interval=self._calculate_confidence_interval(values)
        )

    def _analyze_trends(self, 
                       values: List[float], 
                       dates: List[datetime]) -> Dict:
        """Detailed trend analysis"""
        return {
            "improvement_rate": self._calculate_improvement_rate(values),
            "plateaus": self._identify_plateaus(values, dates),
            "seasonal_pattern": self._analyze_seasonal_patterns(values, dates),
            "peak_performance": self._identify_peak_periods(values, dates),
            "consistency_metrics": self._analyze_performance_consistency(values),
            "fatigue_indicators": self._detect_fatigue_patterns(values, dates)
        }

    def _identify_plateaus(self, values: List[float], dates: List[datetime]) -> List[Dict]:
        """Identify performance plateaus"""
        plateaus = []
        window_size = 3
        threshold = 0.05  # 5% variation threshold

        for i in range(len(values) - window_size + 1):
            window = values[i:i + window_size]
            variation = np.std(window) / np.mean(window)

            if variation < threshold:
                plateaus.append({
                    "start_date": dates[i],
                    "end_date": dates[i + window_size - 1],
                    "mean_value": np.mean(window),
                    "duration_days": (dates[i + window_size - 1] - dates[i]).days
                })

        return plateaus

    def _analyze_seasonal_patterns(self, values: List[float], dates: List[datetime]) -> Dict:
        """Analyze seasonal performance patterns"""
        seasonal_data = {}
        for value, date in zip(values, dates):
            month = date.month
            if month not in seasonal_data:
                seasonal_data[month] = []
            seasonal_data[month].append(value)

        return {
            month: {
                "mean": np.mean(vals),
                "std": np.std(vals),
                "count": len(vals)
            }
            for month, vals in seasonal_data.items()
        }

    def _identify_peak_periods(self, values: List[float], dates: List[datetime]) -> List[Dict]:
        """Identify peak performance periods"""
        peaks = []
        window_size = 5
        
        for i in range(len(values) - window_size + 1):
            window = values[i:i + window_size]
            if np.argmax(window) == window_size // 2:
                peaks.append({
                    "date": dates[i + window_size // 2],
                    "value": values[i + window_size // 2],
                    "improvement": self._calculate_relative_improvement(
                        values[i:i + window_size]
                    )
                })

        return peaks

    def _analyze_performance_consistency(self, values: List[float]) -> Dict:
        """Analyze performance consistency"""
        return {
            "coefficient_of_variation": np.std(values) / np.mean(values) * 100,
            "stability_score": self._calculate_stability_score(values),
            "performance_range": {
                "min": min(values),
                "max": max(values),
                "range": max(values) - min(values)
            }
        }

    def _detect_fatigue_patterns(self, values: List[float], dates: List[datetime]) -> Dict:
        """Detect potential fatigue patterns"""
        decline_threshold = -0.1  # 10% decline
        recovery_threshold = 0.05  # 5% improvement
        
        fatigue_periods = []
        current_decline = []

        for i in range(1, len(values)):
            change = (values[i] - values[i-1]) / values[i-1]
            
            if change < decline_threshold:
                current_decline.append(i)
            elif change > recovery_threshold and current_decline:
                fatigue_periods.append({
                    "start_date": dates[current_decline[0]-1],
                    "end_date": dates[i],
                    "decline_percentage": (values[i] - values[current_decline[0]-1]) / 
                                        values[current_decline[0]-1] * 100
                })
                current_decline = []

        return {
            "fatigue_periods": fatigue_periods,
            "recovery_patterns": self._analyze_recovery_patterns(values, dates)
        }

    def _calculate_stability_score(self, values: List[float]) -> float:
        """Calculate performance stability score (0-100)"""
        cv = np.std(values) / np.mean(values)
        return max(0, min(100, 100 * (1 - cv)))

    def _analyze_recovery_patterns(self, values: List[float], dates: List[datetime]) -> Dict:
        """Analyze recovery patterns after performance declines"""
        recovery_periods = []
        window_size = 3
        
        for i in range(len(values) - window_size + 1):
            window = values[i:i + window_size]
            if window[0] > window[1] and window[2] > window[1]:
                recovery_periods.append({
                    "date": dates[i + 1],
                    "decline": (window[1] - window[0]) / window[0] * 100,
                    "recovery": (window[2] - window[1]) / window[1] * 100,
                    "recovery_time_days": (dates[i + 2] - dates[i + 1]).days
                })

        return recovery_periods