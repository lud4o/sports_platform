from typing import Dict, Any

ANTHROPOMETRIC_TESTS: Dict[str, Dict[str, Dict[str, Any]]] = {
    "BASIC": {
        "height": {"unit": "cm", "required": True},
        "weight": {"unit": "kg", "required": True},
        "standing_reach": {"unit": "cm", "required": True}
    },
    "BODY_COMPOSITION": {
        "neck_circumference": {"unit": "cm", "required": True},
        "waist_circumference": {"unit": "cm", "required": True},
        "hip_circumference": {"unit": "cm", "required": False}  # Required for females
    },
    "MATURATION": {
        "standing_height": {"unit": "cm", "required": True},
        "seated_height": {"unit": "cm", "required": True},
        "weight": {"unit": "kg", "required": True},
        "age": {"unit": "years", "required": True}
    },
    "FV_PROFILE": {
        "leg_length_lying": {"unit": "cm", "required": True},
        "leg_length_squat": {"unit": "cm", "required": True}
    }
}

# Add other test category constants here as well
SPEED_TESTS = {
    "SPRINT": {
        "10m": {"unit": "seconds", "required": True},
        "20m": {"unit": "seconds", "required": True},
        "flying_10m": {"unit": "seconds", "required": False}
    }
}

POWER_TESTS = {
    "JUMPS": {
        "cmj": {"unit": "cm", "required": True},
        "abalakov": {"unit": "cm", "required": True},
        "drop_jump": {
            "jump_height": {"unit": "cm", "required": True},
            "contact_time": {"unit": "ms", "required": True},
            "drop_height": {"unit": "cm", "required": True}
        }
    }
}