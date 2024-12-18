from dataclasses import dataclass
from typing import List, Optional
from domain.testing.entity.test import TestCategory, TestUnit
from domain.testing.entity.value_objects import TestProtocol, AdditionalVariable

@dataclass
class CreateTestCommand:
    name: str
    category: TestCategory
    primary_unit: TestUnit
    description: Optional[str] = None
    protocol: Optional[TestProtocol] = None
    additional_variables: Optional[List[AdditionalVariable]] = None

class CreateTestHandler:
    def __init__(self, test_service: TestManagementService):
        self._test_service = test_service

    def handle(self, command: CreateTestCommand) -> Test:
        return self._test_service.create_test(
            name=command.name,
            category=command.category,
            primary_unit=command.primary_unit,
            description=command.description,
            protocol=command.protocol,
            additional_variables=command.additional_variables
        )