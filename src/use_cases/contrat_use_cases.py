##############################################################################
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

from src.domain.entities.entities import User, Contrat
from src.domain.entities.enums import ContractStatus
from src.domain.entities.exceptions import BusinessRuleViolation
from src.domain.entities.value_objects import Money
from src.domain.interfaces.repository import ContratRepository
from src.domain.policies.user_policy import UserPolicy, RequestPolicy


@dataclass
class CreateContratRequest:
    client_id: int
    commercial_contact_id: int
    contrat_amount: Money
    authorization: RequestPolicy


@dataclass
class CreateContratResponse:
    success: bool
    contrat: Optional[Contrat] = None
    error: Optional[str] = None


class CreateContratUseCase:
    """Use case for creating a new contrat"""

    def __init__(self, contrat_repository: ContratRepository):
        self.repository = contrat_repository

    def execute(self, request: CreateContratRequest) -> CreateContratResponse:

        policy = UserPolicy(request.authorization)
        if not policy.is_allowed():
            return CreateContratResponse(
                success=False,
                error="Seuls les membres gestion peuvent créer des contrats"
            )

        contrat = Contrat(
            id=None,
            client_id=request.client_id,
            commercial_contact_id=request.commercial_contact_id,
            contrat_amount=request.contrat_amount,
            balance_due=request.contrat_amount,
            status=ContractStatus.UNSIGNED,
        )

        saved_contrat = self.repository.save(contrat)
        return CreateContratResponse(success=True, contrat=saved_contrat)

##############################################################################
@dataclass
class UpdateContratRequest:
    contrat_id: int
    contrat_amount: Optional[Money]
    status: Optional[ContractStatus]
    authorization: RequestPolicy


@dataclass
class UpdateContratResponse:
    success: bool
    contrat: Optional[Contrat] = None
    error: Optional[str] = None


class UpdateContratUseCase:
    """Use case for updating a contrat"""
    # TODO A vérifier si utile

    def __init__(self, contrat_repository: ContratRepository):
        self.repository = contrat_repository

    def execute(self, request: UpdateContratRequest) -> UpdateContratResponse:

        contrat = self.repository.find_by_id(request.contrat_id)
        if not contrat:
            return UpdateContratResponse(
                success=False,
                error="Contrat non trouvé"
            )

        policy = UserPolicy(request.authorization)
        request.authorization.context = contrat
        if not policy.is_allowed():
            return UpdateContratResponse(
                success=False,
                error="Seuls les membres gestion peuvent modifier des contrats"
            )



        if request.contrat_amount is not None:
            contrat.contrat_amount = Money(request.contrat_amount)

        if request.status is not None:
            contrat.status = request.status

        updated_contrat = self.repository.save(contrat)
        return UpdateContratResponse(success=True, contrat=updated_contrat)

##############################################################################
class ContratFilter(Enum):
    MINE = "mine"
    NO_SIGN = "no-sign"
    SIGNED = "signed"
    NOT_FULLY_PAID = "not-fully-paid"
    FULLY_PAID = "fully-paid"

@dataclass
class ListContratRequest:
    commercial_contact_id: int
    list_filter: Optional[ContratFilter]

@dataclass
class ListContratResponse:
    success: bool
    contrats: List[Contrat] = None
    error: Optional[str] = None


class ListContratUseCase:
    """Use case for listing contrats"""

    def __init__(self, contrat_repository: ContratRepository):
        self.repository = contrat_repository

    def execute(self, request: ListContratRequest) -> ListContratResponse:
        criteres = dict()
        match request.list_filter:
            case ContratFilter.MINE:
                criteres["commercial_contact_id"] = request.commercial_contact_id
            case ContratFilter.NO_SIGN:
                criteres["signed"] = False
            case ContratFilter.SIGNED:
                criteres["signed"] = True
            case ContratFilter.FULLY_PAID:
                criteres["fully_paid"] = True
            case ContratFilter.NOT_FULLY_PAID:
                criteres["fully_paid"] = False

        contrats = self.repository.find_all(criteres)
        return ListContratResponse(success=True, contrats=contrats)

##############################################################################
@dataclass
class GetContratRequest:
    contrat_id: int


@dataclass
class GetContratResponse:
    success: bool
    contrat: Optional[Contrat] = None
    error: Optional[str] = None


class GetContratUseCase:
    """Use case for retrieving a contrat"""

    def __init__(self, contrat_repository: ContratRepository):
        self.repository = contrat_repository

    def execute(self, request: GetContratRequest) -> GetContratResponse:

        contrat = self.repository.find_by_id(request.contrat_id)
        if not contrat:
            return GetContratResponse(
                success=False,
                error="Contrat non trouvé"
            )

        return GetContratResponse(success=True, contrat=contrat)

##############################################################################
@dataclass
class DeleteContratRequest:
    contrat_id: int
    authorization: RequestPolicy


@dataclass
class DeleteContratResponse:
    success: bool
    error: Optional[str] = None


class DeleteContratUseCase:
    """Use case for deleting a contrat"""

    def __init__(self, contrat_repository: ContratRepository):
        self.repository = contrat_repository

    def execute(self, request: DeleteContratRequest) -> DeleteContratResponse:

        policy = UserPolicy(request.authorization)
        if not policy.is_allowed():
            return DeleteContratResponse(
                success=False,
                error="Seuls les membres administrateur peuvent supprimer des contrats"
            )

        contrat = self.repository.find_by_id(request.contrat_id)
        if not contrat:
            return DeleteContratResponse(
                success=False,
                error="Contrat non trouvé"
            )

        self.repository.delete(contrat.id)
        return DeleteContratResponse(success=True)

##############################################################################

@dataclass
class SignContratRequest:
    contrat_id: int
    authorization: RequestPolicy


@dataclass
class SignContratResponse:
    success: bool
    contrat: Optional[Contrat] = None
    error: Optional[str] = None


class SignContratUseCase:
    """Use case for sign a contrat"""

    def __init__(self, contrat_repository: ContratRepository):
        self.repository = contrat_repository

    def execute(self, request: SignContratRequest) -> SignContratResponse:

        contrat = self.repository.find_by_id(request.contrat_id)
        if not contrat:
            return SignContratResponse(
                success=False,
                error="Contrat non trouvé"
            )

        policy = UserPolicy(request.authorization)
        request.authorization.context = contrat
        if not policy.is_allowed():
            return SignContratResponse(
                success=False,
                error="Seuls les membres "" peuvent supprimer des contrats"
            )

        try:
            contrat.sign()
        except BusinessRuleViolation as e:
            return SignContratResponse(success=False, error=str(e))

        self.repository.save(contrat)
        return SignContratResponse(success=True, contrat=contrat)

##############################################################################
@dataclass
class RecordPaymentContratRequest:
    contrat_id: int
    payment: int
    authorization: RequestPolicy


@dataclass
class RecordPaymentContratResponse:
    success: bool
    contrat: Optional[Contrat] = None
    error: Optional[str] = None


class RecordPaymentContratUseCase:
    """Use case for retrieving a contrat"""

    def __init__(self, contrat_repository: ContratRepository):
        self.repository = contrat_repository

    def execute(self, request: RecordPaymentContratRequest) -> RecordPaymentContratResponse:

        contrat = self.repository.find_by_id(request.contrat_id)
        if not contrat:
            return RecordPaymentContratResponse(
                success=False,
                error="Contrat non trouvé"
            )

        request.authorization.context = contrat
        policy = UserPolicy(request.authorization)
        request.authorization.context = contrat
        if not policy.is_allowed():
            return RecordPaymentContratResponse(
                success=False,
                error="Seuls les membres "" peuvent supprimer des contrats"
            )

        if contrat.is_fully_paid():
            return RecordPaymentContratResponse(
                success=False,
                error="Le contrat a été entièrement réglé"
            )

        try:
            payment = Money(request.payment)
            contrat.record_payment(payment)
        except BusinessRuleViolation as e:
            return RecordPaymentContratResponse(success=False, error=str(e))

        self.repository.save(contrat)
        return RecordPaymentContratResponse(success=True, contrat=contrat)
