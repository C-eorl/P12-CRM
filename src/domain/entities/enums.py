from dataclasses import dataclass
from enum import Enum


class Role(Enum):
    COMMERCIAL = "COMMERCIAL"
    SUPPORT = "SUPPORT"
    GESTION = "GESTION"

class ContractStatus(Enum):
    SIGNED = "SIGNED"
    UNSIGNED = "UNSIGNED"
    CANCELED = "CANCELED"