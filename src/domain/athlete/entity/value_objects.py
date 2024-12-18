from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional
from domain.core.value_object import ValueObject

@dataclass(frozen=True)
class Name(ValueObject):
    first_name: str
    last_name: str

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

@dataclass(frozen=True)
class EmailAddress(ValueObject):
    value: str

    def __post_init__(self):
        if self.value and '@' not in self.value:
            raise ValueError("Invalid email address")