from typing import Dict, List, Optional
from uuid import UUID
import numpy as np
from ..base.base_analyzer import BaseAnalyzer

class ComparativeAnalyzer(BaseAnalyzer):
    def __init__(self, result_repository, group_repository):
        super().__init__(result_repository)
        self._group_repository = group_repository

    def analyze(self,
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