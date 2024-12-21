from typing import Optional, List
from uuid import UUID
from .base import BaseTest, TestConfiguration, TestVariable
from ..value_objects import TestCategory, TestUnit, TestProtocol

class IMTPTest(BaseTest):
    """Isometric Mid-thigh Pull test implementation"""
    def __init__(
        self,
        name: str = "Isometric Mid-thigh Pull",
        description: Optional[str] = None,
        protocol: Optional[TestProtocol] = None,
        id: Optional[UUID] = None
    ):
        config = TestConfiguration(
            requires_equipment=True,
            equipment_list=["Force Platform", "IMTP Rack", "Bar"],
            multiple_trials=True,
            rest_period=180,  # 3 minutes
            requires_warmup=True,
            has_normative_data=True
        )

        variables = [
            TestVariable(
                name="Peak Force",
                unit=TestUnit.NEWTONS,
                is_required=True
            ),
            TestVariable(
                name="RFD 0-50ms",
                unit=TestUnit.NEWTONS_PER_SECOND,
                is_required=True
            ),
            TestVariable(
                name="Force at 200ms",
                unit=TestUnit.NEWTONS,
                is_required=True
            ),
            TestVariable(
                name="Relative Peak Force",
                unit=TestUnit.NEWTONS_PER_KILOGRAM,
                is_required=True,
                calculation_formula="peak_force / body_mass",
                dependent_variables=["body_mass"]
            )
        ]

        super().__init__(
            name=name,
            category=TestCategory.STRENGTH,
            primary_unit=TestUnit.NEWTONS,
            description=description,
            protocol=protocol,
            variables=variables,
            configuration=config,
            id=id
        )

class MaxStrengthTest(BaseTest):
    """1RM test implementation (Squat, Bench Press, etc.)"""
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        protocol: Optional[TestProtocol] = None,
        id: Optional[UUID] = None
    ):
        config = TestConfiguration(
            requires_equipment=True,
            equipment_list=["Barbell", "Weight Plates", "Rack"],
            multiple_trials=False,
            requires_warmup=True,
            has_normative_data=True
        )

        variables = [
            TestVariable(
                name="1RM",
                unit=TestUnit.KILOGRAMS,
                is_required=True
            ),
            TestVariable(
                name="Relative Strength",
                unit=TestUnit.KILOGRAMS,
                is_required=True,
                calculation_formula="weight / body_mass",
                dependent_variables=["body_mass"]
            )
        ]

        super().__init__(
            name=name,
            category=TestCategory.STRENGTH,
            primary_unit=TestUnit.KILOGRAMS,
            description=description,
            protocol=protocol,
            variables=variables,
            configuration=config,
            id=id
        )