from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.entities import Client, User, Contrat, Event
from src.domain.entities.enums import Role
from src.domain.entities.value_objects import Email, Telephone, Money
from src.infrastructures.database.models import ClientModel, UserModel, ContratModel, EventModel


###########################################################################################
#                       CLIENT
###########################################################################################
class SQLAchemyClientRepository:
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

    def find_by_id(self, client_id: int) -> Optional[Client]:
        """Finds a client by its id"""
        db_client = self.session.get(ClientModel, client_id)

        if db_client is None:
            return None
        return self._to_entity(db_client)

    def find_all(self) -> List[Client]:
        """Finds all clients in the database"""
        result = self.session.execute(select(ClientModel))
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
class SQLAchemyUserRepository:
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

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Finds a user by its id"""
        db_user = self.session.get(UserModel, user_id)

        if db_user is None:
            return None
        return self._to_entity(db_user)

    def find_all(self) -> List[User]:
        """Finds all users in the database"""
        result = self.session.execute(select(UserModel))
        db_users = result.scalars().all()

        return [self._to_entity(db_user) for db_user in db_users]

    def find_by_email(self, email: str) -> Optional[User]:
        """Finds a user by email"""
        stmt = select(UserModel).where(UserModel.email == email)
        db_user = self.session.execute(stmt).scalar_one_or_none()

        if db_user is None:
            return None
        return self._to_entity(db_user)

    def find_by_role(self, role: Role) -> List[User]:
        """Finds all user by role"""
        result = self.session.execute(
            select(UserModel).where(UserModel.role == role)
        )
        db_users = result.scalars().all()

        return [self._to_entity(db_user) for db_user in db_users]

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
class SQLAchemyContratRepository:
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

    def find_by_id(self, contrat_id: int) -> Optional[Contrat]:
        """Finds a contrat by its id"""
        db_contrat = self.session.get(ContratModel, contrat_id)

        if db_contrat is None:
            return None
        return self._to_entity(db_contrat)

    def find_all(self) -> List[Contrat]:
        """Finds all contrats in the database"""
        result = self.session.execute(select(ContratModel))
        db_contrats = result.scalars().all()

        return [self._to_entity(db_contrat) for db_contrat in db_contrats]

    def find_by_commercial_contact(self, commercial_contact_id: int) -> List[Contrat]:
        """Finds all contrats by commercial contact"""
        result = self.session.execute(
            select(ContratModel).where(ContratModel.commercial_contact_id == commercial_contact_id)
        )
        db_contrats = result.scalars().all()

        return [self._to_entity(db_contrat) for db_contrat in db_contrats]

    def find_by_client_id(self, client_id: int) -> List[Contrat]:
        """Finds all contrats by client id"""
        result = self.session.execute(
            select(ContratModel).where(ContratModel.client_id == client_id)
        )
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
class SQLAchemyEventRepository:
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

    def find_by_id(self, event_id: int) -> Optional[Event]:
        """Finds a event by its id"""
        db_event = self.session.get(EventModel, event_id)

        if db_event is None:
            return None
        return self._to_entity(db_event)

    def find_all(self) -> List[Event]:
        """Finds all events in the database"""
        result = self.session.execute(select(EventModel))
        db_events = result.scalars().all()

        return [self._to_entity(db_event) for db_event in db_events]

    def find_by_contrat_id(self, contrat_id: int) -> List[Event]:
        """Finds all events by contrat_id"""
        result = self.session.execute(
            select(EventModel).where(EventModel.contrat_id == contrat_id)
        )
        db_events = result.scalars().all()
        return [self._to_entity(db_event) for db_event in db_events]

    def find_by_support_contact_id(self, support_contact_id: int) -> List[Event]:
        """Finds all events by support contact"""
        result = self.session.execute(
            select(EventModel).where(EventModel.support_contact_id == support_contact_id)
        )
        db_events = result.scalars().all()

        return [self._to_entity(db_event) for db_event in db_events]

    def find_by_client_id(self, client_id: int) -> List[Event]:
        """Finds all events by client"""
        result = self.session.execute(
            select(EventModel).where(EventModel.client_id == client_id)
        )
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