from enum import Enum
from typing import Dict, Any

class AnalysisLevel(Enum):
    ELITE = "Elite"
    ADVANCED = "Advanced"
    INTERMEDIATE = "Intermediate"
    DEVELOPING = "Developing"

class AnalysisScope(Enum):
    SINGLE_TEST = "Single Test Analysis"
    MULTI_TEST = "Multi-Test Analysis"
    LONGITUDINAL = "Longitudinal Analysis"
    COMPARATIVE = "Comparative Analysis"

class AnalysisTimeframe(Enum):
    SINGLE = "Single Point"
    RECENT = "Recent History"
    SEASONAL = "Seasonal"
    LONG_TERM = "Long Term"