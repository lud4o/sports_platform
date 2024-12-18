class TestCorrelationAnalyzer:
    def analyze_test_relationships(self,
                                 athlete_id: UUID,
                                 primary_test: str,
                                 related_tests: List[str]) -> Dict:
        """
        Analyze relationships between different tests:
        - Direct correlations
        - Performance predictors
        - Transfer effects
        - Training impact analysis
        """
        results = self._get_multi_test_results(athlete_id, primary_test, related_tests)
        
        return {
            "correlations": self._calculate_test_correlations(results),
            "predictive_factors": self._identify_predictive_tests(results),
            "transfer_effects": self._analyze_transfer_effects(results),
            "training_impact": self._analyze_training_impact(results)
        }