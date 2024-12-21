from typing import Dict, List, Optional
from uuid import UUID
import numpy as np
from ..base.base_analyzer import BaseAnalyzer
from .metrics import (
    JumpMetricsCalculator,
    RSIMetrics, 
    JumpMetrics, 
    ReactiveStrengthLevel,
    ForceVelocityMetrics
)

class JumpProfileAnalyzer(BaseAnalyzer):
    def __init__(self, result_repository):
        super().__init__(result_repository)
        self._metrics_calculator = JumpMetricsCalculator()

    def analyze(self,
                athlete_id: UUID,
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
        # Basic jump analysis
        arm_contribution = self._calculate_arm_contribution(cmj_height, abalakov_height)
        
        # Reactive strength analysis
        reactive_strength = self.analyze_reactive_strength(drop_jumps, cmj_height)
        
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

        # Add force-velocity analysis if data available
        if force_velocity_data:
            profile["force_velocity_profile"] = self._analyze_force_velocity(
                force_velocity_data
            )

        # Add historical analysis
        historical_results = self.get_historical_results(
            athlete_id=athlete_id,
            test_names=["CMJ", "Abalakov Jump"],
            limit=10
        )
        if historical_results:
            profile["trends"] = self.analyze_trend(
                [r['value'] for r in historical_results],
                [r['date'] for r in historical_results]
            )

        return profile

    def analyze_reactive_strength(self, 
                                drop_jumps: List[Dict],
                                cmj_height: float) -> Dict:
        """Analyze reactive strength capabilities"""
        rsi_results = []
        for jump in drop_jumps:
            rsi_metrics = self._metrics_calculator.calculate_rsi(
                jump_height=jump['height'],
                contact_time=jump['contact_time'],
                drop_height=jump.get('drop_height')
            )
            rsi_results.append(rsi_metrics)
        
        # Calculate DJ/CMJ ratio for best drop jump
        best_dj = max(drop_jumps, key=lambda x: x['height'])
        dj_cmj_ratio = self._metrics_calculator.calculate_dj_cmj_ratio(
            best_dj['height'],
            cmj_height
        )
        
        return {
            'rsi_results': [vars(r) for r in rsi_results],
            'dj_cmj_ratio': dj_cmj_ratio,
            'best_rsi': vars(max(rsi_results, key=lambda x: x.rsi_value)),
            'reactive_ability_assessment': self._assess_reactive_ability(
                rsi_results, dj_cmj_ratio
            )
        }

    def _calculate_arm_contribution(self, cmj_height: float, abalakov_height: float) -> float:
        """Calculate arm contribution to jump height in percentage"""
        if cmj_height <= 0:
            return 0
        return ((abalakov_height - cmj_height) / cmj_height) * 100

    def _estimate_power_output(self, jump_height: float) -> float:
        """Estimate power output based on jump height"""
        # Using Sayers equation
        GRAVITY = 9.81
        return (60.7 * jump_height * 100) + 45.3 * GRAVITY  # height in cm

    def _calculate_elastic_energy_usage(self, drop_jumps: List[Dict], cmj_height: float) -> Dict:
        """Calculate elastic energy utilization metrics"""
        best_dj = max(drop_jumps, key=lambda x: x['height'])
        
        return {
            "stretch_shortening_cycle_efficiency": (best_dj['height'] / cmj_height) * 100,
            "contact_time_efficiency": self._assess_contact_time_efficiency(
                best_dj.get('contact_time', 0)
            )
        }

    def _assess_contact_time_efficiency(self, contact_time: float) -> str:
        """Assess contact time efficiency"""
        if contact_time <= 0.2:
            return "excellent"
        elif contact_time <= 0.25:
            return "good"
        elif contact_time <= 0.3:
            return "moderate"
        return "needs_improvement"

    def _assess_reactive_ability(self, rsi_results: List['RSIMetrics'], dj_cmj_ratio: Dict) -> str:
        """Assess overall reactive ability"""
        best_rsi = max(rsi_results, key=lambda x: x.rsi_value)
        
        if best_rsi.quality == "elite" and dj_cmj_ratio['ratio'] >= 1.1:
            return "elite_reactive_strength"
        elif best_rsi.quality in ["elite", "advanced"] and dj_cmj_ratio['ratio'] >= 1.0:
            return "advanced_reactive_strength"
        elif best_rsi.quality == "intermediate" and dj_cmj_ratio['ratio'] >= 0.9:
            return "intermediate_reactive_strength"
        return "developing_reactive_strength"

    def _analyze_force_velocity(self, force_velocity_data: List[Dict]) -> Dict:
        """
        Force-velocity analysis from jump data
        
        Args:
            force_velocity_data: List of dicts containing:
                - height: Jump height in meters
                - added_weight: Additional load in kg
                - body_mass: Athlete's body mass in kg
        """
        if not force_velocity_data or len(force_velocity_data) < 2:
            return {"status": "insufficient_data"}

        # Extract values for analysis
        heights = [jump['height'] for jump in force_velocity_data]
        weights = [jump['added_weight'] for jump in force_velocity_data]
        body_mass = force_velocity_data[0]['body_mass']

        # Calculate velocities and forces
        velocities = [np.sqrt(2 * 9.81 * h) for h in heights]
        forces = [(body_mass + w) * 9.81 for w in weights]

        # Linear regression
        slope, intercept, r_value, _, _ = stats.linregress(velocities, forces)

        # Calculate key parameters
        f0 = intercept  # Force at zero velocity
        v0 = -intercept/slope  # Velocity at zero force
        pmax = (f0 * v0) / 4  # Maximum power

        return {
            "force_velocity_profile": {
                "f0": round(f0, 2),
                "v0": round(v0, 2),
                "pmax": round(pmax, 2),
                "sfv": round(-slope, 2),
                "r_squared": round(r_value**2, 3)
            },
            "load_velocity_points": [
                {"load": w, "velocity": v} 
                for w, v in zip(weights, velocities)
            ],
            "profile_quality": self._assess_fv_profile_quality(r_value**2)
        }
    
    def _assess_fv_profile_quality(self, r_squared: float) -> str:
        """Assess quality of F-V profile based on R² value"""
        if r_squared >= 0.95:
            return "excellent"
        elif r_squared >= 0.90:
            return "good"
        elif r_squared >= 0.85:
            return "acceptable"
        return "needs_improvement"