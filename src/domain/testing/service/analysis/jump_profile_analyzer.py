class JumpProfileAnalyzer:
    def analyze_jump_profile(self,
                           cmj_height: float,
                           abalakov_height: float,
                           drop_jumps: List[Dict],
                           force_velocity_data: Optional[List[Dict]] = None) -> Dict:
        """
        Comprehensive jump analysis including:
        - Arm contribution to jump (Abalakov vs CMJ)
        - Reactive strength capabilities (from drop jumps)
        - Force-velocity profiling
        - Elastic energy utilization
        - Power output estimations
        """
        arm_contribution = self._calculate_arm_contribution(cmj_height, abalakov_height)
        reactive_strength = self._analyze_reactive_strength(drop_jumps)
        
        profile = {
            "vertical_jump_capacity": {
                "cmj_height": cmj_height,
                "abalakov_height": abalakov_height,
                "arm_contribution_percent": arm_contribution,
                "power_estimation": self._estimate_power_output(cmj_height)
            },
            "reactive_strength": reactive_strength,
            "elastic_energy_utilization": self._calculate_elastic_energy_usage(
                drop_jumps, cmj_height
            )
        }

        if force_velocity_data:
            profile["force_velocity_profile"] = self._analyze_force_velocity(
                force_velocity_data
            )

        return profile