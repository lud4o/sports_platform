class JumpTest(BaseTest):
    """Jump test implementation"""
    def __init__(
        self,
        name: str,
        has_arm_swing: bool,
        description: Optional[str] = None,
        protocol: Optional[TestProtocol] = None,
        id: Optional[UUID] = None
    ):
        config = TestConfiguration(
            requires_equipment=True,
            equipment_list=["Jump Mat", "Force Platform"],
            multiple_trials=True,
            rest_period=60,
            requires_warmup=True
        )

        variables = [
            TestVariable(
                name="Flight Time",
                unit=TestUnit.SECONDS,
                is_required=True
            ),
            TestVariable(
                name="Jump Height",
                unit=TestUnit.CENTIMETERS,
                is_required=True,
                calculation_formula="9.81 * flight_time^2 / 8"
            )
        ]

        super().__init__(
            name=name,
            category=TestCategory.POWER,
            primary_unit=TestUnit.CENTIMETERS,
            description=description,
            protocol=protocol,
            variables=variables,
            configuration=config,
            id=id
        )
        self._has_arm_swing = has_arm_swing