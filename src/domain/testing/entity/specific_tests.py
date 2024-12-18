from typing import Optional
from uuid import UUID
from .test import Test
from .value_objects import TestCategory, TestUnit, TestProtocol, AdditionalVariable

class StrengthTest(Test):
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        protocol: Optional[TestProtocol] = None,
        id: Optional[UUID] = None
    ):
        additional_vars = []
        
        if name == "IMTP":
            additional_vars = [
                AdditionalVariable("RFD 0-50ms", TestUnit.NEWTONS_PER_SECOND, True),
                AdditionalVariable("Force at 200ms", TestUnit.NEWTONS, True),
                AdditionalVariable("Relative Peak Force", TestUnit.NEWTONS_PER_KILOGRAM, True)
            ]
        elif "1RM" in name:  # For back squat, bench press etc.
            additional_vars = [
                AdditionalVariable(
                    name="Relative Strength",
                    unit=TestUnit.KILOGRAMS,
                    calculation_formula="weight/body_mass",
                    dependent_variables=["body_mass"]
                )
            ]

        super().__init__(
            name=name,
            category=TestCategory.STRENGTH,
            primary_unit=TestUnit.KILOGRAMS if "1RM" in name else TestUnit.NEWTONS,
            description=description,
            protocol=protocol,
            additional_variables=additional_vars,
            id=id
        )

class EnduranceTest(Test):
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        protocol: Optional[TestProtocol] = None,
        id: Optional[UUID] = None
    ):
        additional_vars = []
        
        if name == "Beep Test":
            additional_vars = [
                AdditionalVariable(
                    name="VO2 Max Estimate",
                    unit=TestUnit.LEVEL,
                    is_required=False,
                    calculation_formula="calculate_vo2_max(level, shuttle)"
                )
            ]
        elif name == "Cooper Test":
            additional_vars = [
                AdditionalVariable(
                    name="VO2 Max Estimate",
                    unit=TestUnit.KILOMETERS,
                    is_required=False,
                    calculation_formula="calculate_cooper_vo2_max(distance)"
                )
            ]

        super().__init__(
            name=name,
            category=TestCategory.ENDURANCE,
            primary_unit=TestUnit.LEVEL if name == "Beep Test" else TestUnit.KILOMETERS,
            description=description,
            protocol=protocol,
            additional_variables=additional_vars,
            id=id
        )

class FlexibilityTest(Test):
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        protocol: Optional[TestProtocol] = None,
        id: Optional[UUID] = None
    ):
        super().__init__(
            name=name,
            category=TestCategory.FLEXIBILITY,
            primary_unit=TestUnit.CENTIMETERS,
            description=description,
            protocol=protocol,
            id=id
        )