from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime
from ..entity.tests.base import BaseTest
from .test_factory import TestFactory

class TestService:
    """Service for managing tests and test results"""
    
    def __init__(self, test_repository, result_repository):
        self._test_repository = test_repository
        self._result_repository = result_repository
        self._test_factory = TestFactory()

    def create_test(self,
                   test_type: str,
                   name: Optional[str] = None,
                   description: Optional[str] = None,
                   protocol: Optional[dict] = None,
                   **kwargs) -> BaseTest:
        """Create a new test"""
        test = self._test_factory.create_test(
            test_type=test_type,
            name=name,
            description=description,
            protocol=protocol,
            **kwargs
        )
        
        if test:
            return self._test_repository.save(test)
        raise ValueError(f"Invalid test type: {test_type}")

    def record_test_result(self,
                          test_id: UUID,
                          athlete_id: UUID,
                          primary_value: float,
                          additional_values: Optional[Dict] = None,
                          test_date: Optional[datetime] = None) -> Dict:
        """Record a test result"""
        test = self._test_repository.get(test_id)
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

        # Combine all values
        all_values = {
            "primary_value": primary_value,
            **(additional_values or {}),
            **derived_values
        }

        # Save result
        return self._result_repository.save_result(
            test_id=test_id,
            athlete_id=athlete_id,
            values=all_values,
            test_date=test_date or datetime.utcnow()
        )

    def get_test_configurations(self) -> Dict:
        """Get configurations for all available tests"""
        return self._test_factory.get_available_test_types()

    def get_tests_by_category(self, category: str) -> List[str]:
        """Get all tests in a specific category"""
        return self._test_factory.get_test_by_category(category)