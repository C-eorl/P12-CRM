from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Role(Enum):
    COMMERCIAL = "COMMERCIAL"
    SUPPORT = "SUPPORT"
    GESTION = "GESTION"