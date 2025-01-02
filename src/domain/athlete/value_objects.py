from enum import Enum
from dataclasses import dataclass
from ..core.value_object import ValueObject

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"

@dataclass(frozen=True)
class Name(ValueObject):
    first_name: str
    last_name: str

@dataclass(frozen=True)
class EmailAddress(ValueObject):
    email: str