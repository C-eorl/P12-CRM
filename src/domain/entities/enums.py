from enum import Enum

######################################################################
#                       Enumération métier                           #
######################################################################

class Role(Enum):
    COMMERCIAL = "COMMERCIAL"
    SUPPORT = "SUPPORT"
    GESTION = "GESTION"
    ADMIN = "ADMIN"

class ContractStatus(Enum):
    SIGNED = "SIGNED"
    UNSIGNED = "UNSIGNED"