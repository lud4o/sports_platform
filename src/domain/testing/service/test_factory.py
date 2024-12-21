from typing import Dict, List, Optional, Type, Union
from uuid import UUID
from ..entity.test import Test
from ..entity.value_objects import (
    TestCategory, 
    TestUnit, 
    TestProtocol, 
    AdditionalVariable,
    TestEnvironment
)
from ..entity.tests.base import TestConfiguration

class TestFactory:
    """Factory for creating and managing test instances"""
    
    _test_types: Dict[str, Type[Test]] = {
        # Speed tests
        "sprint_10m": Test,
        "sprint_20m": Test,
        "flying_10m": Test,
        
        # Power tests
        "cmj": Test,
        "abalakov": Test,
        "drop_jump": Test,
        
        # Strength tests
        "imtp": Test,
        "back_squat_1rm": Test,
        "bench_press_1rm": Test,
        
        # Anthropometric tests
        "basic_anthropometrics": Test,
        "body_composition": Test,
        "maturation": Test
    }

    @classmethod
    def create_test(cls, 
                   test_type: str, 
                   name: Optional[str] = None,
                   description: Optional[str] = None,
                   **kwargs) -> Optional[Test]:
        """Create a test instance with complete configuration"""
        if test_type not in cls._test_types:
            return None

        if not name:
            name = test_type.replace('_', ' ').title()

        # Get complete test configuration
        category, unit, config = cls._get_test_config(test_type)
        
        return Test(
            name=name,
            category=category,
            primary_unit=unit,
            description=description,
            protocol=config.get("protocol"),
            additional_variables=config.get("variables", []),
            **kwargs
        )

    @classmethod
    def register_test_type(cls, type_name: str, test_class: Type[Test]):
        """Register a new test type"""
        cls._test_types[type_name] = test_class

    @classmethod
    def get_available_test_types(cls) -> Dict[str, Dict]:
        """Get all available test types with their configurations"""
        return {
            test_type: {
                "category": cls._get_test_config(test_type)[0].value,
                "unit": cls._get_test_config(test_type)[1].value,
                "name": test_type.replace('_', ' ').title()
            }
            for test_type in cls._test_types.keys()
        }

    @classmethod
    def get_test_by_category(cls, category: str) -> List[str]:
        """Get all test types in a specific category"""
        return [
            test_type for test_type in cls._test_types.keys()
            if cls._get_test_config(test_type)[0].name == category
        ]

    @classmethod
    def _get_test_config(cls, test_type: str) -> tuple[TestCategory, TestUnit, Dict]:
        """Get complete configuration for a test type"""
        base_configs = {
            # Speed tests
            "sprint_10m": {
                "category": TestCategory.SPEED,
                "unit": TestUnit.SECONDS,
                "protocol": TestProtocol(
                    name="10m Sprint Protocol",
                    description="Standard 10m sprint test",
                    setup_instructions="Set up timing gates at 0m and 10m",
                    required_equipment=["Timing Gates", "Sprint Track"]
                ),
                "variables": [
                    AdditionalVariable("Reaction Time", TestUnit.SECONDS, False),
                    AdditionalVariable("Split Times", TestUnit.SECONDS, False)
                ]
            },

            # Power tests
            "cmj": {
                "category": TestCategory.POWER,
                "unit": TestUnit.CENTIMETERS,
                "protocol": TestProtocol(
                    name="Countermovement Jump Protocol",
                    description="Standard CMJ test",
                    setup_instructions="Use force platform or jump mat",
                    required_equipment=["Force Platform/Jump Mat"]
                ),
                "variables": [
                    AdditionalVariable("Flight Time", TestUnit.SECONDS, True),
                    AdditionalVariable("Peak Power", TestUnit.WATTS, False),
                    AdditionalVariable("Peak Force", TestUnit.NEWTONS, False)
                ]
            },

            # Strength tests
            "imtp": {
                "category": TestCategory.STRENGTH,
                "unit": TestUnit.NEWTONS,
                "protocol": TestProtocol(
                    name="IMTP Protocol",
                    description="Isometric Mid-thigh Pull test",
                    setup_instructions="Set bar height to mid-thigh position",
                    required_equipment=["Force Platform", "IMTP Rack", "Bar"]
                ),
                "variables": [
                    AdditionalVariable("RFD 0-50ms", TestUnit.NEWTONS_PER_SECOND, True),
                    AdditionalVariable("Force at 200ms", TestUnit.NEWTONS, True),
                    AdditionalVariable("Relative Peak Force", TestUnit.NEWTONS_PER_KILOGRAM, True)
                ]
            },

            # Add configurations for other tests...
        }

        config = base_configs.get(test_type)
        if config:
            return (config["category"], config["unit"], {
                "protocol": config.get("protocol"),
                "variables": config.get("variables", []),
                "configuration": TestConfiguration(
                    requires_equipment=bool(config.get("protocol").required_equipment),
                    equipment_list=config.get("protocol").required_equipment,
                    multiple_trials="trials" in config,
                    requires_warmup=True
                )
            })
        return (TestCategory.SPEED, TestUnit.SECONDS, {})  # Default config