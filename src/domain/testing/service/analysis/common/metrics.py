from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

class TrendDirection(Enum):
    IMPROVING = "Improving"
    STABLE = "Stable"
    DECLINING = "Declining"
    INCONSISTENT = "Inconsistent"

@dataclass
class PerformanceMetrics:
    current_value: float
    personal_best: float
    improvement_rate: float
    percentile_rank: float
    relative_to_benchmark: float
    trend_direction: TrendDirection
    confidence_interval: tuple

@dataclass
class TrendAnalysis:
    slope: float
    r_squared: float
    prediction_next: float
    confidence_band: tuple