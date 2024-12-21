from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime
from ..entity.test import Test, TestCategory, TestUnit
from ..entity.value_objects import TestProtocol, AdditionalVariable
from ..repository.test_repository import TestRepository
from .test_factory import TestFactory

# Analyzer imports
from .analysis.strength.imtp_analyzer import IMTPAnalyzer, IMTPResult
from .analysis.test_analyzer_factory import TestAnalyzerFactory

class TestManagementService:
    """Service for managing tests, test definitions, and analysis"""
    
    def __init__(self, repository: TestRepository):
        self._repository = repository
        self._test_factory = TestFactory()
        self._analyzer_factory = TestAnalyzerFactory(repository)
        self._imtp_analyzer = IMTPAnalyzer()

    # Test Definition Management
    def create_test(self,
                   name: str,
                   category: TestCategory,
                   primary_unit: TestUnit,
                   description: Optional[str] = None,
                   protocol: Optional[TestProtocol] = None,
                   additional_variables: List[AdditionalVariable] = None) -> Test:
        """Create a new test definition"""
        # Check if test with same name exists
        if self._repository.find_by_name(name):
            raise ValueError(f"Test with name {name} already exists")

        test = Test(
            name=name,
            category=category,
            primary_unit=primary_unit,
            description=description,
            protocol=protocol,
            additional_variables=additional_variables
        )

        return self._repository.save(test)

    def create_predefined_test(self,
                             test_type: str,
                             name: Optional[str] = None,
                             description: Optional[str] = None,
                             protocol: Optional[dict] = None,
                             **kwargs) -> Test:
        """Create a predefined test type"""
        test = self._test_factory.create_test(
            test_type=test_type,
            name=name,
            description=description,
            protocol=protocol,
            **kwargs
        )
        
        if test:
            return self._repository.save(test)
        raise ValueError(f"Invalid test type: {test_type}")

    def update_test(self,
                   test_id: UUID,
                   name: Optional[str] = None,
                   description: Optional[str] = None,
                   protocol: Optional[TestProtocol] = None,
                   additional_variables: Optional[List[AdditionalVariable]] = None) -> Test:
        """Update existing test definition"""
        test = self._repository.get(test_id)
        if not test:
            raise ValueError(f"Test with id {test_id} not found")

        # Validate new name doesn't conflict with existing tests
        if name and name != test.name:
            existing = self._repository.find_by_name(name)
            if existing and existing.id != test_id:
                raise ValueError(f"Test with name {name} already exists")

        # Update test properties
        updated_test = Test(
            id=test.id,
            name=name or test.name,
            category=test.category,
            primary_unit=test.primary_unit,
            description=description or test.description,
            protocol=protocol or test.protocol,
            additional_variables=additional_variables or test.additional_variables
        )

        return self._repository.save(updated_test)

    # Test Results and Analysis
    def record_test_result(self,
                          test_id: UUID,
                          athlete_id: UUID,
                          primary_value: float,
                          additional_values: Optional[Dict] = None,
                          test_date: Optional[datetime] = None) -> Dict:
        """Record a test result"""
        test = self._repository.get(test_id)
        if not test:
            raise ValueError(f"Test not found: {test_id}")

        # Validate primary value
        if not test.validate_result(primary_value):
            raise ValueError(f"Invalid primary value for test: {primary_value}")

        # Validate and calculate additional values
        if additional_values:
            for name, value in additional_values.items():
                if not test.validate_result(value, name):
                    raise ValueError(f"Invalid value for {name}: {value}")

        # Calculate derived variables
        derived_values = test.calculate_derived_variables(
            primary_value,
            additional_values or {}
        )

        # Get appropriate analyzer and analyze results
        analyzer = self._analyzer_factory.get_analyzer(test)
        analysis_result = None
        if analyzer:
            analysis_result = analyzer.analyze(
                athlete_id=athlete_id,
                test_date=test_date or datetime.utcnow(),
                primary_value=primary_value,
                additional_values={**additional_values, **derived_values} if additional_values else derived_values
            )

        # Combine all values
        result = {
            "primary_value": primary_value,
            **(additional_values or {}),
            **derived_values
        }

        # Save result
        saved_result = self._repository.save_result(
            test_id=test_id,
            athlete_id=athlete_id,
            values=result,
            test_date=test_date or datetime.utcnow()
        )

        return {
            "result": saved_result,
            "analysis": analysis_result
        }

    # Specific Test Analysis Methods
    def analyze_imtp_result(self,
                          athlete_id: UUID,
                          peak_force: float,
                          rfd_50: float,
                          force_200ms: float,
                          body_mass: float,
                          test_date: datetime = None) -> Dict:
        """Analyze IMTP test results"""
        if test_date is None:
            test_date = datetime.now()

        result = IMTPResult(
            peak_force=peak_force,
            relative_peak_force=peak_force / (body_mass * 9.81),
            rfd_50=rfd_50,
            force_200ms=force_200ms,
            test_date=test_date,
            athlete_id=athlete_id
        )

        return self._imtp_analyzer.analyze_result(result)

    # Query Methods
    def get_tests_by_category(self, category: TestCategory) -> List[Test]:
        """Get all tests in a specific category"""
        return self._repository.find_by_category(category)

    def get_available_categories(self) -> List[TestCategory]:
        """Get list of all available test categories"""
        return list(TestCategory)

    def get_available_test_types(self) -> Dict:
        """Get configurations for all available predefined tests"""
        return self._test_factory.get_available_test_types()

    # Analysis Methods
    def analyze_test_relationships(self,
                                 athlete_id: UUID,
                                 tests: List[UUID],
                                 time_period: Optional[tuple] = None) -> Dict:
        """Analyze relationships between different tests"""
        correlation_analyzer = self._analyzer_factory.get_common_analyzer("correlations")
        return correlation_analyzer.analyze(
            athlete_id=athlete_id,
            test_ids=tests,
            time_period=time_period
        )

    def analyze_performance_trends(self,
                                 athlete_id: UUID,
                                 test_id: UUID,
                                 time_period: Optional[tuple] = None) -> Dict:
        """Analyze performance trends for a specific test"""
        performance_analyzer = self._analyzer_factory.get_common_analyzer("performance")
        return performance_analyzer.analyze(
            athlete_id=athlete_id,
            test_id=test_id,
            time_period=time_period
        )