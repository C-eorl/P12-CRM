from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.domain.entities.enums import Role
from src.domain.entities.value_objects import Email, Telephone


@dataclass
class User:
    id: Optional[int]
    full_name: str
    email: Email
    password: str
    role: Role

    def is_commercial(self) -> bool:
        return self.role == Role.COMMERCIAL

    def is_support(self) -> bool:
        return self.role == Role.SUPPORT

    def is_gestion(self) -> bool:
        return self.role == Role.GESTION


@dataclass
class Client:
    id: Optional[int]
    fullname: str
    email: Email
    telephone: Telephone
    company_name: str
    commercial_contact: User

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

    def can_be_updated(self, user: User) -> bool:
        if user.id == self.commercial_contact.id:
            return True
        if user.role == Role.COMMERCIAL:
            return True
        return False

@dataclass
class Contrat:
    id: int
    client: Client
    commercial_contact: User
    contrat_amount: int
    balance_due: int
    signed: bool


@dataclass
class Event:
    name: str
    id: int
    contrat_id: int
    client_name: str
    contact_client: Optional[Email, Telephone]
    support_contact: User
    location: str
    attendees: int
    notes: str
