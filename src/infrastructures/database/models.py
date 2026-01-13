import enum
from typing import List

from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase): ...

class Role(enum.Enum):
    COMMERCIAL = "commercial"
    SUPPORT = "support"
    GESTION = "gestion"

class UserModel(Base):
    """Model SQLAlchemy User"""
    __tablename__ = "users"

    id: Mapped[int]= mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    created_at: Mapped[DateTime] = Column(DateTime, nullable=False)

    clients: Mapped[List["ClientModel"]] = relationship(back_populates="commercial_contact")
    contrats: Mapped[List["ContratModel"]] = relationship(back_populates="commercial_contact")
    events: Mapped[List["EventModel"]] = relationship(back_populates="support_contact")


    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"


class ClientModel(Base):
    """Model SQLAlchemy Client"""
    __tablename__ = "clients"

    id: Mapped[int]= mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    telephone: Mapped[str] = mapped_column(String, nullable=False)
    company_name: Mapped[str] = mapped_column(String, nullable=False)

    commercial_contact_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    commercial_contact: Mapped[UserModel] = relationship(back_populates="clients")

    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"<Client(id={self.id}, fullname='{self.fullname}')>"


class ContratModel(Base):
    """Model SQLAlchemy Contrat"""
    __tablename__ = "contrats"

    id: Mapped[int]= mapped_column(primary_key=True)

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    client: Mapped[ClientModel] = relationship(back_populates="contrats")

    commercial_contact_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    commercial_contact: Mapped[UserModel] = relationship(back_populates="contrats")

    contrat_amount: Mapped[int]= mapped_column(Integer, nullable=False)
    balance_due: Mapped[int]= mapped_column(Integer, nullable=False)
    signed: Mapped[bool] = mapped_column(Boolean, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"<Contrat(id={self.id}, client={self.client}, commercial_contact={self.commercial_contact})>"


class EventModel(Base):
    """Model SQLAlchemy Event"""
    __tablename__ = "events"

    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    contrat_id: Mapped[int] = mapped_column(ForeignKey("contrats.id"), nullable=False)
    contrat: Mapped[ContratModel] = relationship(back_populates="events")

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    client: Mapped[ClientModel] = relationship(back_populates="events")

    support_contact_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    support_contact: Mapped[UserModel] = relationship(back_populates="events")

    location: Mapped[str] = mapped_column(String, nullable=False)
    attendees: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"<Event(id={self.id}, name={self.name})>"
