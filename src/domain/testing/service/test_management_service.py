from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime
from ..entity.test import Test, TestCategory, TestUnit
from ..entity.value_objects import TestProtocol, AdditionalVariable
from .analysis.strength_analyzer import IMTPAnalyzer, IMTPResult
from ..repository.test_repository import TestRepository

class TestManagementService:
    def __init__(self, repository: TestRepository):
        self._repository = repository
        self._imtp_analyzer = IMTPAnalyzer()

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

    def get_tests_by_category(self, category: TestCategory) -> List[Test]:
        """Get all tests in a specific category"""
        return self._repository.find_by_category(category)

    def get_available_categories(self) -> List[TestCategory]:
        """Get list of all available test categories"""
        return list(TestCategory)

    def analyze_imtp_result(self,
                          athlete_id: UUID,
                          peak_force: float,
                          rfd_50: float,
                          force_200ms: float,
                          body_mass: float,
                          test_date: datetime = None) -> Dict:
        """
        Analyze IMTP test results
        
        Args:
            athlete_id: UUID of the athlete
            peak_force: Maximum force recorded (N)
            rfd_50: Rate of force development at 50ms (N/s)
            force_200ms: Force at 200ms (N)
            body_mass: Athlete's body mass (kg)
            test_date: Date of the test (defaults to current datetime)
        
        Returns:
            Dictionary containing analysis results
        """
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