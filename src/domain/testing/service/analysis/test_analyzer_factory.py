from typing import Optional, Type
from domain.testing.entity.test import Test
from domain.testing.entity.value_objects import TestCategory
from .base.base_analyzer import BaseAnalyzer

# Common analyzers
from .common.performance_analyzer import PerformanceAnalyzer
from .common.factor_analyzer import PerformanceFactorAnalyzer
from .common.comparative_analyzer import ComparativeAnalyzer
from .common.test_correlation_analyzer import TestCorrelationAnalyzer

# Speed analyzers
from .speed.sprint_analyzer import SprintAnalyzer
from .speed.speed_acceleration_profiler import SpeedAccelerationProfiler

# Power analyzers
from .power.jump_profile_analyzer import JumpProfileAnalyzer
from .power.force_velocity_analyzer import ForceVelocityAnalyzer

# Strength analyzers
from .strength.strength_analyzer import StrengthAnalyzer
from .strength.imtp_analyzer import IMTPAnalyzer

# Anthropometric analyzers
from .anthropometrics.anthropometric_analyzer import AnthropometricAnalyzer
from .anthropometrics.body_composition_analyzer import BodyCompositionAnalyzer
from .anthropometrics.maturation_analyzer import MaturationAnalyzer

class TestAnalyzerFactory:
    """Factory for creating test analyzers with proper dependencies"""
    
    _analyzers = {
        TestCategory.SPEED: SprintAnalyzer,
        TestCategory.POWER: JumpProfileAnalyzer,
        TestCategory.STRENGTH: StrengthAnalyzer,
        TestCategory.ANTHROPOMETRICS: AnthropometricAnalyzer
    }

    _common_analyzers = {
        "performance": PerformanceAnalyzer,
        "factors": PerformanceFactorAnalyzer,
        "comparative": ComparativeAnalyzer,
        "correlations": TestCorrelationAnalyzer
    }

    def __init__(self, result_repository):
        self._result_repository = result_repository

    def get_analyzer(self, test: Test) -> Optional[BaseAnalyzer]:
        """Get appropriate analyzer for test type"""
        analyzer_class = self._analyzers.get(test.category)
        if analyzer_class:
            return analyzer_class(self._result_repository)
        return None

    @classmethod
    def register_analyzer(cls, category: TestCategory, analyzer_class: Type[BaseAnalyzer]):
        """Register a new analyzer for a test category"""
        cls._analyzers[category] = analyzer_class