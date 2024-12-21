from typing import Optional
from uuid import UUID
from .base import BaseTest, TestConfiguration, TestVariable
from ..value_objects import TestCategory, TestUnit, TestProtocol

class SprintTest(BaseTest):
    """Sprint test implementation"""
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        protocol: Optional[TestProtocol] = None,
        id: Optional[UUID] = None
    ):
        config = TestConfiguration(
            requires_equipment=True,
            equipment_list=["Timing Gates"],
            multiple_trials=True,
            rest_period=180,  # 3 minutes
            requires_warmup=True
        )

        super().__init__(
            name=name,
            category=TestCategory.SPEED,
            primary_unit=TestUnit.SECONDS,
            description=description,
            protocol=protocol,
            configuration=config,
            id=id
        )