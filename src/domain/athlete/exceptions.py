class AthleteError(Exception):
    """Base exception for athlete domain"""
    pass

class InvalidAgeGroupError(AthleteError):
    """Raised when an invalid age group is specified"""
    pass

class EmailRequiredError(AthleteError):
    """Raised when attempting operations requiring email without one set"""
    pass