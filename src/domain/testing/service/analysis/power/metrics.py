from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class ReactiveStrengthLevel(Enum):
    ELITE = "Elite"
    ADVANCED = "Advanced"
    INTERMEDIATE = "Intermediate"
    DEVELOPING = "Developing"

@dataclass
class JumpMetrics:
    height: float
    type: str  # CMJ, Abalakov, Drop Jump
    contact_time: Optional[float] = None
    drop_height: Optional[float] = None
    added_weight: Optional[float] = None

@dataclass
class RSIMetrics:
    jump_height: float
    contact_time: float
    drop_height: float
    rsi_value: float
    rsi_modified: Optional[float] = None
    quality: str

@dataclass
class ForceVelocityMetrics:
    force: float
    velocity: float
    power: float
    added_weight: float
    body_mass: float
    height: Optional[float] = None  # Jump height if available
    f0: Optional[float] = None  # Theoretical maximum force
    v0: Optional[float] = None  # Theoretical maximum velocity

class JumpMetricsCalculator:
    """Calculator for various jump-related metrics including RSI"""
    
    RSI_THRESHOLDS = {
        "elite": 3.0,
        "advanced": 2.5,
        "intermediate": 2.0,
        "developing": 1.5
    }
    
    def calculate_rsi(self, 
                     jump_height: float, 
                     contact_time: float,
                     drop_height: Optional[float] = None) -> RSIMetrics:
        """
        Calculate Reactive Strength Index metrics
        
        Args:
            jump_height: Jump height in meters
            contact_time: Ground contact time in seconds
            drop_height: Drop height in meters (for modified RSI)
        """
        # Basic RSI calculation
        rsi = jump_height / contact_time if contact_time > 0 else 0
        
        # Modified RSI if drop height is provided
        rsi_modified = None
        if drop_height is not None:
            rsi_modified = jump_height / (contact_time * drop_height)
        
        # Determine quality level
        quality = self._assess_rsi_quality(rsi)
        
        return RSIMetrics(
            jump_height=jump_height,
            contact_time=contact_time,
            drop_height=drop_height,
            rsi_value=rsi,
            rsi_modified=rsi_modified,
            quality=quality
        )
    
    def calculate_dj_cmj_ratio(self, dj_height: float, cmj_height: float) -> Dict:
        """Calculate Drop Jump to CMJ ratio and assess reactive ability"""
        ratio = dj_height / cmj_height if cmj_height > 0 else 0
        
        return {
            'ratio': ratio,
            'assessment': self._assess_dj_cmj_ratio(ratio),
            'dj_height': dj_height,
            'cmj_height': cmj_height
        }
    
    def _assess_rsi_quality(self, rsi: float) -> str:
        """Assess RSI quality based on thresholds"""
        if rsi >= self.RSI_THRESHOLDS["elite"]:
            return "elite"
        elif rsi >= self.RSI_THRESHOLDS["advanced"]:
            return "advanced"
        elif rsi >= self.RSI_THRESHOLDS["intermediate"]:
            return "intermediate"
        return "developing"
    
    def _assess_dj_cmj_ratio(self, ratio: float) -> str:
        """Assess DJ/CMJ ratio quality"""
        if ratio >= 1.1:
            return "excellent_reactive_ability"
        elif ratio >= 1.0:
            return "good_reactive_ability"
        elif ratio >= 0.9:
            return "moderate_reactive_ability"
        return "limited_reactive_ability"