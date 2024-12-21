from typing import Dict, List, Optional, Tuple
from uuid import UUID
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler
from ..base.base_analyzer import BaseAnalyzer

class PerformanceFactorAnalyzer(BaseAnalyzer):
    def __init__(self, result_repository):
        super().__init__(result_repository)
        self.test_names = []

    def analyze(self, 
               athlete_id: UUID,
               time_period: Optional[tuple] = None) -> Dict:
        """
        Analyze athlete's performance factors across different tests
        Returns factor loadings and correlations between tests
        """
        # Get all test results for the athlete
        results = self._result_repository.get_athlete_results_by_category(
            athlete_id=athlete_id,
            time_period=time_period
        )

        # Prepare data for analysis
        data, self.test_names = self._prepare_data_matrix(results)
        
        # Perform factor analysis
        factor_loadings = self._perform_factor_analysis(data)
        
        # Calculate correlations
        correlations = self._calculate_correlations(data)
        
        # Identify primary performance factors
        performance_factors = self._identify_performance_factors(factor_loadings)

        return {
            "factor_loadings": factor_loadings,
            "correlations": correlations,
            "performance_factors": performance_factors,
            "recommendations": self._generate_recommendations(performance_factors)
        }

    def _prepare_data_matrix(self, results: Dict) -> Tuple[np.ndarray, List[str]]:
        """Prepare and normalize data for analysis"""
        data_matrix = []
        test_names = []
        
        for category, tests in results.items():
            for test_name, values in tests.items():
                test_names.append(test_name)
                # Normalize values to account for different measurement scales
                normalized_values = StandardScaler().fit_transform(
                    np.array(values).reshape(-1, 1)
                ).ravel()
                data_matrix.append(normalized_values)

        return np.array(data_matrix).T, test_names

    def _perform_factor_analysis(self, data: np.ndarray) -> Dict:
        """Perform factor analysis on performance data"""
        fa = FactorAnalysis(n_components=3, random_state=42)
        fa.fit(data)
        
        # Transform factor loadings into interpretable results
        loadings = pd.DataFrame(
            fa.components_.T,
            columns=['Power', 'Speed', 'Endurance'],
            index=self.test_names
        )

        return {
            "loadings": loadings,
            "variance_explained": fa.explained_variance_ratio_,
            "communalities": fa.communalities_
        }

    def _calculate_correlations(self, data: np.ndarray) -> Dict:
        """Calculate correlations between different tests"""
        correlations = {}
        n_tests = len(self.test_names)
        
        for i in range(n_tests):
            correlations[self.test_names[i]] = {}
            for j in range(n_tests):
                if i != j:
                    corr, p_value = pearsonr(data[:, i], data[:, j])
                    correlations[self.test_names[i]][self.test_names[j]] = {
                        "correlation": round(corr, 3),
                        "p_value": round(p_value, 3)
                    }

        return correlations