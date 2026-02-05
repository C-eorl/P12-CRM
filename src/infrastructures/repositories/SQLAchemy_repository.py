from typing import List, Optional

from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from src.domain.entities.entities import Client, User, Contrat, Event
from src.domain.entities.enums import Role, ContractStatus
from src.domain.entities.value_objects import Email, Telephone, Money
from src.infrastructures.database.models import ClientModel, UserModel, ContratModel, EventModel


###########################################################################################
#                       CLIENT
###########################################################################################
class SQLAlchemyClientRepository:
    """SQL Alchemy Client repository """
    def __init__(self, session: Session):
        self.session = session

    def save(self, client: Client) -> Client:
        """Creates a new client or modifie a client, and saves it to the database"""
        if client.id is None:

            db_client = ClientModel(
                fullname=client.fullname,
                email=str(client.email),
                telephone=str(client.telephone),
                company_name=client.company_name,
                commercial_contact_id=client.commercial_contact_id,
                created_at=client.created_at,
                updated_at=client.updated_at,
            )
            self.session.add(db_client)

        else:
            db_client = self.session.get(ClientModel, client.id)

            db_client.fullname = client.fullname
            db_client.email = str(client.email)
            db_client.telephone = str(client.telephone)
            db_client.company_name = client.company_name
            db_client.updated_at = client.updated_at


        self.session.commit()
        return self._to_entity(db_client)

    def exist(self, client_id: int) -> bool:
        """Checks if a client exists in the database"""
        stmt = select(exists().where(ClientModel.id == client_id))
        return self.session.execute(stmt).scalar()

    def find_by_id(self, client_id: int) -> Optional[Client]:
        """Finds a client by its id"""
        db_client = self.session.get(ClientModel, client_id)

        if db_client is None:
            return None
        return self._to_entity(db_client)

    def find_all(self, criteres: dict) -> List[Client]:
        """Finds all clients in the database"""
        stmt = select(ClientModel)

        commercial_contact_id = criteres.get("commercial_contact_id")
        if commercial_contact_id is not None:
            stmt = stmt.where(
                ClientModel.commercial_contact_id == commercial_contact_id
            )

        result = self.session.execute(stmt)
        db_clients = result.scalars().all()

        return [self._to_entity(db_client) for db_client in db_clients]

    def delete(self, client_id: int) -> None:
        """Deletes a client from the database"""
        find_client = self.session.get(ClientModel, client_id)
        self.session.delete(find_client)
        self.session.commit()

    @staticmethod
    def _to_entity(model: ClientModel) -> Client:
        """Converts a database client to a domain entity"""
        return Client(
            id=model.id,
            fullname=model.fullname,
            email=Email(model.email),
            telephone=Telephone(model.telephone),
            company_name=model.company_name,
            commercial_contact_id=model.commercial_contact_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

###########################################################################################
#                       USER
###########################################################################################
class SQLAlchemyUserRepository:
    """SQL Alchemy User repository """
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        """Creates a new user or modifie a user, and saves it to the database"""
        if user.id is None:

            db_user = UserModel(
                fullname=user.fullname,
                email=str(user.email),
                password=user.password,
                role=user.role,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            self.session.add(db_user)

        else:
            db_user = self.session.get(UserModel, user.id)

            db_user.fullname = user.fullname
            db_user.email = str(user.email)
            db_user.password = user.password
            db_user.role = user.role
            db_user.updated_at = user.updated_at


        self.session.commit()
        return self._to_entity(db_user)

    def exist(self, user_id: int) -> bool:
        """Checks if a user exists in the database"""
        stmt = select(exists().where(UserModel.id == user_id))
        return self.session.execute(stmt).scalar()

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Finds a user by its id"""
        db_user = self.session.get(UserModel, user_id)

        if db_user is None:
            return None
        return self._to_entity(db_user)

    def find_all(self, criteres: dict) -> List[User]:
        """Finds all users in the database"""
        stmt = select(UserModel)

        if criteres["role"] is not None:
            stmt = stmt.where(UserModel.role == criteres["role"])

        result = self.session.execute(stmt)
        db_users = result.scalars().all()

        return [self._to_entity(db_user) for db_user in db_users]

    def find_by_email(self, email: str) -> Optional[User]:
        """Finds a user by email"""
        stmt = select(UserModel).where(UserModel.email == email)
        db_user = self.session.execute(stmt).scalar_one_or_none()

        if db_user is None:
            return None
        return self._to_entity(db_user)

    def delete(self, user_id: int) -> None:
        """Deletes a user from the database"""
        find_user = self.session.get(UserModel, user_id)
        self.session.delete(find_user)
        self.session.commit()


    @staticmethod
    def _to_entity(model: UserModel) -> User:
        """Converts a database user to a domain entity"""
        return User(
            id=model.id,
            fullname=model.fullname,
            email=Email(model.email),
            password=model.password,
            role=Role(model.role),
            created_at=model.created_at,
            updated_at=model.updated_at
        )

###########################################################################################
#                       CONTRAT
###########################################################################################
class SQLAlchemyContratRepository:
    """SQL Alchemy Contrat repository """
    def __init__(self, session: Session):
        self.session = session

    def save(self, contrat: Contrat) -> Contrat:
        """Creates a new contrat or modified a contrat, and saves it to the database"""
        if contrat.id is None:

            db_contrat = ContratModel(
                client_id = contrat.client_id,
                commercial_contact_id = contrat.commercial_contact_id,
                contrat_amount = int(contrat.contrat_amount.amount),
                balance_due = int(contrat.balance_due.amount),
                status = contrat.status,
                created_at=contrat.created_at,
                updated_at=contrat.updated_at
            )
            self.session.add(db_contrat)

        else:
            db_contrat = self.session.get(ContratModel, contrat.id)

            db_contrat.client_id = contrat.client_id
            db_contrat.commercial_contact_id = contrat.commercial_contact_id
            db_contrat.contrat_amount = int(contrat.contrat_amount.amount)
            db_contrat.balance_due = int(contrat.balance_due.amount)
            db_contrat.status = contrat.status
            db_contrat.updated_at = contrat.updated_at


        self.session.commit()
        return self._to_entity(db_contrat)

    def exist(self, contrat_id: int) -> bool:
        """Checks if a contrat exists in the database"""
        stmt = select(exists().where(ContratModel.id == contrat_id))
        return self.session.execute(stmt).scalar()

    def find_by_id(self, contrat_id: int) -> Optional[Contrat]:
        """Finds a contrat by its id"""
        db_contrat = self.session.get(ContratModel, contrat_id)

        if db_contrat is None:
            return None
        return self._to_entity(db_contrat)

    def find_all(self, criteres) -> List[Contrat]:
        """Finds all contrats in the database"""
        stmt = select(ContratModel)
        if criteres.get("commercial_contact_id"):
            stmt = stmt.where(ContratModel.commercial_contact_id == criteres["commercial_contact_id"])

        if criteres.get("signed") is True:
            stmt = stmt.where(ContratModel.status == ContractStatus.SIGNED)

        if criteres.get("signed") is False:
            stmt = stmt.where(ContratModel.status == ContractStatus.UNSIGNED)

        if criteres.get("fully_paid") is True:
            stmt = stmt.where(ContratModel.balance_due == 0)

        if criteres.get("fully_paid") is False:
            stmt = stmt.where(ContratModel.balance_due != 0)

        result = self.session.execute(stmt)
        db_contrats = result.scalars().all()

        return [self._to_entity(db_contrat) for db_contrat in db_contrats]


    def delete(self, contrat_id: int) -> None:
        """Deletes a contrat"""
        find_contrat = self.session.get(ContratModel, contrat_id)
        self.session.delete(find_contrat)
        self.session.commit()


    @staticmethod
    def _to_entity(model: ContratModel) -> Contrat:
        """Converts a model Contrat to a domain Contrat"""
        return Contrat(
            id=model.id,
            client_id=model.client_id,
            commercial_contact_id=model.commercial_contact_id,
            contrat_amount=Money(model.contrat_amount),
            balance_due=Money(model.balance_due),
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

###########################################################################################
#                       EVENT
###########################################################################################
class SQLAlchemyEventRepository:
    """SQL Alchemy Event repository """

    def __init__(self, session: Session):
        self.session = session

    def save(self, event: Event) -> Event:
        """Creates a new event or modified a event, and saves it to the database"""
        if event.id is None:

            db_event = EventModel(
                name=event.name,
                contrat_id=event.contrat_id,
                client_id=event.client_id,
                support_contact_id=event.support_contact_id,
                start_date=event.start_date,
                end_date=event.end_date,
                location=event.location,
                attendees=event.attendees,
                notes=event.notes,
                created_at=event.created_at,
                updated_at=event.updated_at
            )
            self.session.add(db_event)

        else:
            db_event = self.session.get(EventModel, event.id)

            db_event.name = event.name
            db_event.contrat_id=event.contrat_id
            db_event.client_id=event.client_id
            db_event.support_contact_id=event.support_contact_id
            db_event.start_date=event.start_date
            db_event.end_date=event.end_date
            db_event.location=event.location
            db_event.attendees=event.attendees
            db_event.notes=event.notes
            db_event.updated_at = event.updated_at


        self.session.commit()
        return self._to_entity(db_event)

    def exist(self, event_id: int) -> bool:
        """Checks if a client exists in the database"""
        stmt = select(exists().where(EventModel.id == event_id))
        return self.session.execute(stmt).scalar()

    def find_by_id(self, event_id: int) -> Optional[Event]:
        """Finds event by its id"""
        db_event = self.session.get(EventModel, event_id)

        if db_event is None:
            return None
        return self._to_entity(db_event)

    def find_all(self, criteres) -> List[Event]:
        """Finds all events in the database"""
        stmt = select(EventModel)
        if criteres.get("support_contact_id"):
            stmt = stmt.where(EventModel.support_contact_id == criteres["support_contact_id"])

        if criteres.get("support_contact") is False:
            stmt = stmt.where(EventModel.support_contact_id == None)

        result = self.session.execute(stmt)
        db_events = result.scalars().all()

        return [self._to_entity(db_event) for db_event in db_events]

    def delete(self, event_id: int) -> None:
        """Deletes an event"""
        find_event = self.session.get(EventModel, event_id)
        self.session.delete(find_event)
        self.session.commit()


    @staticmethod
    def _to_entity(model: EventModel) -> Event:
        """Converts a SQLAlchemy Event model to a domain Event"""
        return Event(
            id=model.id,
            name=model.name,
            contrat_id=model.contrat_id,
            client_id=model.client_id,
            support_contact_id=model.support_contact_id,
            start_date=model.start_date,
            end_date=model.end_date,
            location=model.location,
            attendees=model.attendees,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at
        )