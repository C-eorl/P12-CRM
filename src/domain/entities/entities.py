from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.domain.entities.enums import Role, ContractStatus
from src.domain.entities.exceptions import BusinessRuleViolation
from src.domain.entities.value_objects import Email, Telephone, Money


@dataclass
class User:
    id: Optional[int]
    full_name: str
    email: Email
    password: str
    role: Role

    def is_commercial(self) -> bool:
        return self.role is Role.COMMERCIAL

    def is_support(self) -> bool:
        return self.role is Role.SUPPORT

    def is_gestion(self) -> bool:
        return self.role is Role.GESTION

    # TODO ajout d'un UserPolicy pour les permission si besoin


@dataclass
class Client:
    id: Optional[int]
    fullname: str
    email: Email
    telephone: Telephone
    company_name: str
    commercial_contact_id: int

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update_info(self, fullname: Optional[str], email: Optional[Email],
                    telephone: Optional[Telephone], company_name: Optional[str]):
        if fullname:
            self.fullname = fullname
        if email:
            self.email = email
        if telephone:
            self.telephone = telephone
        if company_name:
            self.company_name = company_name
        self.updated_at = datetime.now()

    def can_be_updated_by(self, user: User) -> bool:
        if user.id == self.commercial_contact_id:
            return True
        return False

@dataclass
class Contrat:
    id: Optional[int]
    client: int
    commercial_contact_id: int
    contrat_amount: Money
    balance_due: Money
    status: ContractStatus

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def sign(self):
        """Sign the contrat"""
        if self.status == ContractStatus.SIGNED:
            raise BusinessRuleViolation("Contrat déjà signé")
        self.status = ContractStatus.SIGNED

    def record_payment(self, payment: Money):
        if payment > self.balance_due:
            raise BusinessRuleViolation(
                "Le montant est plus grand que le reste à payer"
            )

        self.balance_due = self.balance_due - payment

    def is_fully_paid(self) -> bool:
        return self.balance_due.amount == 0

    def can_be_updated_by(self, user: User) -> bool:
        """Verified if user can be updated"""
        if user.id == self.commercial_contact_id:
            return True
        if user.is_gestion():
            return True
        return False

    def __str__(self):
        return f"Contrat #{self.id} - {self.status} ({self.contrat_amount})"

@dataclass
class Event:
    id: Optional[int]
    name: str
    contrat_id: int
    client_id: int
    support_contact_id: Optional[int]
    start_date: datetime
    end_date: datetime
    location: str
    attendees: int
    notes: str

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validation"""
        if self.start_date < datetime.now():
            raise BusinessRuleViolation(
                "La date de début est déjà passé"
            )
        if self.end_date <= self.start_date:
            raise BusinessRuleViolation(
                "La date de fin doit être après la date de début"
            )
        if self.attendees <= 0:
            raise BusinessRuleViolation(
                "Le nombre de participants doit être positif"
            )

    def assign_support(self, user: User):
        """Assigned support user for this event"""
        if not user.is_support():
            raise PermissionError(
                "Seul les membre du support peut être assigné à un évènement"
            )
        self.support_contact_id = user.id

    def has_support_contact(self) -> bool:
        """Verified if assigned support user"""
        return self.support_contact_id is not None

    def can_be_updated_by(self, user: User) -> bool:
        """Verified if user can be updated"""
        if user.is_gestion():
            return True
        if user.is_support() and user.id == self.support_contact_id:
            return True
        return False

    def update_info(self, name: Optional[str], location: Optional[str],
                    attendees: Optional[int], notes: Optional[str]):
        """Updates info about the event"""
        if name is not None:
            if not isinstance(name, str):
                raise BusinessRuleViolation("Le nom doit être du texte")
            if not name.strip():
                raise BusinessRuleViolation("le nom ne peut pas être vide")
            self.name = name
        if location is not None:
            if not isinstance(name, str):
                raise BusinessRuleViolation("Le lieu doit être du texte")
            if not name.strip():
                raise BusinessRuleViolation("le nom ne peut pas être vide")
            self.location = location
        if attendees is not None:
            if not isinstance(attendees, int):
                raise BusinessRuleViolation("Le nombre de participant doit être un nombre")
            if attendees <= 0:
                raise BusinessRuleViolation(
                    "Le nombre de participants doit être positif"
                )
            self.attendees = attendees
        if notes is not None:
            if not isinstance(name, str):
                raise BusinessRuleViolation("Les notes doivent être du texte")
            self.notes = notes

    def __str__(self):
        support = f"Support: {self.support_contact_id}" if self.support_contact_id else "Sans Support"
        return f"Event: {self.name} - {self.start_date.strftime('%d/%m/%Y')} ({support})"
