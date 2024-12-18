class BodyCompositionAnalyzer:
    def calculate_body_fat(self,
                         gender: str,
                         waist_circ: float,
                         neck_circ: float,
                         height: float,
                         hip_circ: Optional[float] = None) -> float:
        """
        Calculate body fat percentage using Navy method
        All measurements in centimeters
        """
        if gender.lower() == 'male':
            return 495 / (1.0324 - 0.19077 * np.log10(waist_circ - neck_circ) + 
                         0.15456 * np.log10(height)) - 450
        else:
            if hip_circ is None:
                raise ValueError("Hip circumference required for female calculation")
            return 495 / (1.29579 - 0.35004 * np.log10(waist_circ + hip_circ - neck_circ) +
                         0.22100 * np.log10(height)) - 450

    def calculate_phv(self,
                     height: float,
                     seated_height: float,
                     weight: float,
                     age: float) -> float:
        """Calculate Peak Height Velocity score"""
        # Mirwald equation implementation
        leg_length = height - seated_height
        sitting_height_ratio = (seated_height / height) * 100
        
        return -9.236 + (0.0002708 * (leg_length * sitting_height_ratio)) + \
               (-0.001663 * (age * leg_length)) + \
               (0.007216 * (age * sitting_height_ratio)) + \
               (0.02292 * (weight / height * 100))