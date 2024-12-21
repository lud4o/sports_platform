from typing import Dict, List, Optional
from uuid import UUID
import numpy as np
from scipy import stats
from ..base.base_analyzer import BaseAnalyzer

class TestCorrelationAnalyzer(BaseAnalyzer):
    def analyze(self,
               athlete_id: UUID,
               primary_test: str,
               related_tests: List[str]) -> Dict:
        """
        Analyze relationships between different tests
        
        Args:
            athlete_id: Athlete's UUID
            primary_test: Main test to analyze
            related_tests: List of tests to analyze relationships with
        """
        results = self._get_multi_test_results(athlete_id, primary_test, related_tests)
        
        correlations = self._calculate_test_correlations(results)
        predictive_factors = self._identify_predictive_tests(results)
        transfer_effects = self._analyze_transfer_effects(results)
        
        return {
            "correlations": correlations,
            "predictive_factors": predictive_factors,
            "transfer_effects": transfer_effects,
            "training_impact": self._analyze_training_impact(results),
            "recommendations": self._generate_recommendations(
                correlations,
                predictive_factors,
                transfer_effects
            )
        }

    def _calculate_test_correlations(self, results: Dict) -> Dict:
        """Calculate correlations between tests"""
        correlations = {}
        test_names = list(results.keys())
        
        for i, test1 in enumerate(test_names):
            correlations[test1] = {}
            for test2 in test_names[i+1:]:
                correlation = self._calculate_correlation(
                    results[test1],
                    results[test2]
                )
                correlations[test1][test2] = correlation
                correlations.setdefault(test2, {})[test1] = correlation

        return correlations

    def _calculate_correlation(self, values1: List[float], values2: List[float]) -> Dict:
        """Calculate detailed correlation metrics between two tests"""
        correlation, p_value = stats.pearsonr(values1, values2)
        spearman_corr, spearman_p = stats.spearmanr(values1, values2)
        
        return {
            "pearson": {
                "coefficient": round(correlation, 3),
                "p_value": round(p_value, 3)
            },
            "spearman": {
                "coefficient": round(spearman_corr, 3),
                "p_value": round(spearman_p, 3)
            },
            "relationship_strength": self._evaluate_relationship_strength(correlation),
            "significance": p_value < 0.05
        }

    def _identify_predictive_tests(self, results: Dict) -> Dict:
        """Identify tests that might predict performance in others"""
        predictive_relationships = {}
        test_names = list(results.keys())
        
        for predictor in test_names:
            for target in test_names:
                if predictor != target:
                    prediction_strength = self._analyze_predictive_strength(
                        results[predictor],
                        results[target]
                    )
                    if prediction_strength["r_squared"] > 0.5:  # Threshold for strong prediction
                        predictive_relationships[f"{predictor}->{target}"] = prediction_strength

        return predictive_relationships

    def _analyze_predictive_strength(self, predictor: List[float], target: List[float]) -> Dict:
        """Analyze how well one test predicts another"""
        slope, intercept, r_value, p_value, std_err = stats.linregress(predictor, target)
        
        return {
            "r_squared": r_value**2,
            "slope": slope,
            "p_value": p_value,
            "std_error": std_err,
            "equation": f"y = {slope:.3f}x + {intercept:.3f}"
        }

    def _analyze_transfer_effects(self, results: Dict) -> Dict:
        """Analyze potential transfer effects between tests"""
        transfer_effects = {}
        
        for test1, values1 in results.items():
            for test2, values2 in results.items():
                if test1 != test2:
                    transfer = self._calculate_transfer_effect(values1, values2)
                    if transfer["effect_size"] > 0.3:  # Medium effect size threshold
                        transfer_effects[f"{test1}->{test2}"] = transfer

        return transfer_effects

    def _calculate_transfer_effect(self, values1: List[float], values2: List[float]) -> Dict:
        """Calculate transfer effect between two tests"""
        # Calculate Cohen's d effect size
        mean_diff = np.mean(values1) - np.mean(values2)
        pooled_std = np.sqrt((np.var(values1) + np.var(values2)) / 2)
        effect_size = mean_diff / pooled_std if pooled_std != 0 else 0

        return {
            "effect_size": effect_size,
            "effect_magnitude": self._evaluate_effect_magnitude(effect_size),
            "confidence_interval": self._calculate_effect_ci(effect_size, len(values1))
        }

    def _evaluate_relationship_strength(self, correlation: float) -> str:
        """Evaluate the strength of a correlation"""
        abs_corr = abs(correlation)
        if abs_corr >= 0.7:
            return "strong"
        elif abs_corr >= 0.5:
            return "moderate"
        elif abs_corr >= 0.3:
            return "weak"
        return "negligible"

    def _evaluate_effect_magnitude(self, effect_size: float) -> str:
        """Evaluate the magnitude of an effect size"""
        abs_effect = abs(effect_size)
        if abs_effect >= 0.8:
            return "large"
        elif abs_effect >= 0.5:
            return "medium"
        elif abs_effect >= 0.2:
            return "small"
        return "negligible"

    def _calculate_effect_ci(self, effect_size: float, n: int, confidence: float = 0.95) -> tuple:
        """Calculate confidence interval for effect size"""
        se = np.sqrt((4/n) * (1 + (effect_size**2)/8))
        ci = stats.norm.interval(confidence, loc=effect_size, scale=se)
        return (float(ci[0]), float(ci[1]))  # Convert np.float64 to float