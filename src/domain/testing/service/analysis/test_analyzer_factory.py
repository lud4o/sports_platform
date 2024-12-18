from typing import Optional
from domain.testing.entity.test import Test
from domain.testing.entity.value_objects import TestCategory
from domain.testing.service.analysis.sprint_analyzer import SprintAnalyzer
from domain.testing.service.analysis.strength_analyzer import StrengthAnalyzer

class TestAnalyzerFactory:
    """Factory for creating appropriate test analyzers"""
    
    def __init__(self, result_repository):
        self._result_repository = result_repository
    
    def get_analyzer(self, test: Test) -> Optional[object]:
        """Get appropriate analyzer for test type"""
        if test.category == TestCategory.SPEED:
            return SprintAnalyzer(self._result_repository)
        elif test.category == TestCategory.STRENGTH:
            return StrengthAnalyzer(self._result_repository)
        
        return None