from typing import Dict, List, Optional
from uuid import UUID
import numpy as np
from scipy import stats
from ..base.base_analyzer import BaseAnalyzer
from .metrics import ForceVelocityMetrics

class ForceVelocityAnalyzer(BaseAnalyzer):
    def __init__(self, result_repository):
        super().__init__(result_repository)

    def analyze(self,
              athlete_id: UUID,
              jump_results: List[Dict[str, float]],
              athlete_mass: float,
              leg_length: float) -> Dict:
        """Main analysis method implementing BaseAnalyzer.analyze"""
        return self.calculate_fv_profile(athlete_id, jump_results, athlete_mass, leg_length)

    def calculate_fv_profile(self,
                           athlete_id: UUID,
                           jump_results: List[Dict[str, float]],
                           athlete_mass: float,
                           leg_length: float) -> Dict:
        """
        Calculate Force-Velocity profile using Samozino's method
        jump_results should contain: {height: float, added_weight: float}
        """
        # Implementation of Samozino's method
        heights = [result['height'] for result in jump_results]
        weights = [result['added_weight'] for result in jump_results]
        
        # Calculate velocity and force for each jump
        velocities = [np.sqrt(2 * 9.81 * h) for h in heights]
        forces = [(athlete_mass + w) * 9.81 for w in weights]
        
        # Linear regression to find F0 and V0
        slope, intercept, r_value, p_value, std_err = stats.linregress(velocities, forces)
        
        # Calculate profile parameters
        f0 = intercept  # Force at zero velocity
        v0 = -intercept/slope  # Velocity at zero force
        pmax = (f0 * v0) / 4  # Maximum power
        sfv = -slope  # Force-velocity slope
        
        profile = {
            'f0': f0,
            'v0': v0,
            'pmax': pmax,
            'sfv': sfv,
            'r_squared': r_value**2,
            'optimal_slope': self._calculate_optimal_slope(leg_length),
            'imbalance': self._calculate_fv_imbalance(sfv, leg_length)
        }

        # Add trend analysis if historical data available
        historical_results = self.get_historical_results(
            athlete_id=athlete_id,
            test_names=["Loaded Jump"],
            limit=10
        )

        if historical_results:
            profile["trends"] = self.analyze_trend(
                [r['pmax'] for r in historical_results],
                [r['date'] for r in historical_results]
            )

        return profile

    def _calculate_optimal_slope(self, leg_length: float) -> float:
        """
        Calculate optimal F-V slope based on leg length
        Based on Samozino et al. (2012, 2014) research
        
        Args:
            leg_length: Length of the lower limb in meters
        Returns:
            Optimal slope value in N.s/m
        """
        # Constants from research
        GRAVITY = 9.81
        OPTIMAL_PUSH_OFF_DISTANCE = 0.4  # 40% of leg length
        
        # Calculate optimal push-off distance
        h_po = leg_length * OPTIMAL_PUSH_OFF_DISTANCE
        
        # Calculate optimal slope (SFV_opt)
        # Formula from Samozino et al. (2014)
        optimal_slope = -(GRAVITY * leg_length) / (4 * h_po)
        
        return optimal_slope

    def _calculate_fv_imbalance(self, actual_slope: float, leg_length: float) -> float:
        """
        Calculate Force-Velocity imbalance percentage
        
        Args:
            actual_slope: Measured F-V slope
            leg_length: Length of the lower limb in meters
        Returns:
            Imbalance percentage (-ve: force deficit, +ve: velocity deficit)
        """
        optimal_slope = self._calculate_optimal_slope(leg_length)
        imbalance = ((actual_slope - optimal_slope) / optimal_slope) * 100
        
        return {
            'imbalance_percentage': imbalance,
            'deficit_type': 'force' if imbalance < 0 else 'velocity',
            'magnitude': abs(imbalance),
            'optimal_slope': optimal_slope,
            'actual_slope': actual_slope
        }