from typing import Dict, List
import numpy as np
from scipy.stats import pearsonr
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler

class PerformanceFactorAnalyzer:
    def __init__(self, result_repository):
        self._result_repository = result_repository

    def analyze_performance_factors(self, 
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
        data = self._prepare_data_matrix(results)
        
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

    def _prepare_data_matrix(self, results: Dict) -> np.ndarray:
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

class ComparativeAnalyzer:
    def __init__(self, result_repository, group_repository):
        self._result_repository = result_repository
        self._group_repository = group_repository

    def analyze_athlete_vs_group(self,
                               athlete_id: UUID,
                               group_id: Optional[UUID] = None,
                               comparison_type: str = "age_group") -> Dict:
        """
        Compare athlete's performance with a group
        comparison_type can be: 'age_group', 'team', 'custom_group', 'sport'
        """
        # Get athlete's results
        athlete_results = self._result_repository.get_athlete_results(athlete_id)
        
        # Get comparison group results
        if group_id:
            group_results = self._get_group_results(group_id)
        else:
            group_results = self._get_comparison_group_results(
                athlete_id, comparison_type
            )

        # Calculate percentile ranks and z-scores
        rankings = self._calculate_rankings(athlete_results, group_results)
        
        # Identify strengths and weaknesses
        analysis = self._analyze_performance_profile(rankings)
        
        # Generate specific recommendations
        recommendations = self._generate_recommendations(analysis)

        return {
            "rankings": rankings,
            "analysis": analysis,
            "recommendations": recommendations,
            "group_statistics": self._calculate_group_statistics(group_results)
        }

    def _calculate_rankings(self, 
                          athlete_results: Dict, 
                          group_results: Dict) -> Dict:
        """Calculate percentile ranks and z-scores for each test"""
        rankings = {}
        
        for test_id, result in athlete_results.items():
            group_values = group_results.get(test_id, [])
            if group_values:
                rankings[test_id] = {
                    "percentile": self._calculate_percentile(
                        result.value, group_values
                    ),
                    "z_score": self._calculate_z_score(
                        result.value, group_values
                    ),
                    "relative_performance": self._evaluate_relative_performance(
                        result.value, group_values
                    )
                }

        return rankings

    def _evaluate_relative_performance(self, 
                                    value: float, 
                                    group_values: List[float]) -> str:
        """Evaluate performance relative to the group"""
        z_score = self._calculate_z_score(value, group_values)
        
        if z_score > 2:
            return "Exceptional"
        elif z_score > 1:
            return "Above Average"
        elif z_score > -1:
            return "Average"
        elif z_score > -2:
            return "Below Average"
        else:
            return "Needs Improvement"