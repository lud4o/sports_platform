from typing import Optional, List
from uuid import UUID
from .base import BaseTest, TestConfiguration, TestVariable
from ..value_objects import TestCategory, TestUnit, TestProtocol

class BasicAnthropometricTest(BaseTest):
    """Basic anthropometric measurements"""
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        protocol: Optional[TestProtocol] = None,
        id: Optional[UUID] = None
    ):
        config = TestConfiguration(
            requires_equipment=True,
            equipment_list=["Stadiometer", "Scale", "Measuring Tape"],
            multiple_trials=False,
            has_normative_data=True
        )

        variables = [
            TestVariable(
                name="Height",
                unit=TestUnit.CENTIMETERS,
                is_required=True
            ),
            TestVariable(
                name="Weight",
                unit=TestUnit.KILOGRAMS,
                is_required=True
            ),
            TestVariable(
                name="Standing Reach",
                unit=TestUnit.CENTIMETERS,
                is_required=True
            )
        ]

        super().__init__(
            name=name,
            category=TestCategory.ANTHROPOMETRICS,
            primary_unit=TestUnit.CENTIMETERS,
            description=description,
            protocol=protocol,
            variables=variables,
            configuration=config,
            id=id
        )

class BodyCompositionTest(BaseTest):
    """Body composition assessment"""
    def __init__(
        self,
        name: str = "Body Composition",
        description: Optional[str] = None,
        protocol: Optional[TestProtocol] = None,
        id: Optional[UUID] = None
    ):
        config = TestConfiguration(
            requires_equipment=True,
            equipment_list=["Measuring Tape"],
            multiple_trials=False,
            has_normative_data=True
        )

        variables = [
            TestVariable(
                name="Waist Circumference",
                unit=TestUnit.CENTIMETERS,
                is_required=True
            ),
            TestVariable(
                name="Neck Circumference",
                unit=TestUnit.CENTIMETERS,
                is_required=True
            ),
            TestVariable(
                name="Hip Circumference",
                unit=TestUnit.CENTIMETERS,
                is_required=False  # Required for females only
            ),
            TestVariable(
                name="Body Fat Percentage",
                unit=TestUnit.PERCENTAGE,
                is_required=True,
                calculation_formula="navy_formula",  # Implemented in analyzer
                dependent_variables=["waist_circumference", "neck_circumference", "height", "hip_circumference"]
            )
        ]

        super().__init__(
            name=name,
            category=TestCategory.ANTHROPOMETRICS,
            primary_unit=TestUnit.PERCENTAGE,
            description=description,
            protocol=protocol,
            variables=variables,
            configuration=config,
            id=id
        )

class MaturationTest(BaseTest):
    """PHV and maturation assessment"""
    def __init__(
        self,
        name: str = "Maturation Assessment",
        description: Optional[str] = None,
        protocol: Optional[TestProtocol] = None,
        id: Optional[UUID] = None
    ):
        config = TestConfiguration(
            requires_equipment=True,
            equipment_list=["Stadiometer", "Scale"],
            multiple_trials=False,
            has_normative_data=True
        )

        variables = [
            TestVariable(
                name="Standing Height",
                unit=TestUnit.CENTIMETERS,
                is_required=True
            ),
            TestVariable(
                name="Seated Height",
                unit=TestUnit.CENTIMETERS,
                is_required=True
            ),
            TestVariable(
                name="Weight",
                unit=TestUnit.KILOGRAMS,
                is_required=True
            ),
            TestVariable(
                name="PHV Score",
                unit=TestUnit.SCORE,
                is_required=True,
                calculation_formula="calculate_phv",  # Implemented in analyzer
                dependent_variables=["standing_height", "seated_height", "weight", "age"]
            ),
            TestVariable(
                name="Leg Length",
                unit=TestUnit.CENTIMETERS,
                is_required=True,
                calculation_formula="standing_height - seated_height",
                dependent_variables=["standing_height", "seated_height"]
            )
        ]

        super().__init__(
            name=name,
            category=TestCategory.ANTHROPOMETRICS,
            primary_unit=TestUnit.SCORE,
            description=description,
            protocol=protocol,
            variables=variables,
            configuration=config,
            id=id
        )