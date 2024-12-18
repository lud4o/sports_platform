class PerformanceTrendAnalyzer:
    def analyze_performance_trends(self,
                                 athlete_id: UUID,
                                 test_type: str,
                                 time_period: Optional[tuple] = None) -> Dict:
        """
        Advanced trend analysis including:
        - Rate of improvement
        - Performance plateaus identification
        - Seasonal variations
        - Peak performance timing
        - Performance consistency
        - Fatigue indicators
        """
        results = self._get_performance_history(athlete_id, test_type, time_period)
        
        return {
            "improvement_rate": self._calculate_improvement_rate(results),
            "plateaus": self._identify_plateaus(results),
            "seasonal_pattern": self._analyze_seasonal_patterns(results),
            "peak_performance": self._identify_peak_periods(results),
            "consistency_metrics": self._analyze_performance_consistency(results),
            "fatigue_indicators": self._detect_fatigue_patterns(results)
        }