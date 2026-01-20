from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.entities import Client
from src.domain.entities.value_objects import Email, Telephone
from src.infrastructures.database.models import ClientModel


class SQLAchemyClientRepository:
    """SQL Alchemy repository"""
    def __init__(self, session: Session):
        self.session = session

    def save(self, client: Client) -> Client:
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
        db_client = self.session.get(ClientModel, client_id)

        if db_client is None:
            return None
        return self._to_entity(db_client)

    def find_all(self) -> List[Client]:
        result = self.session.execute(select(ClientModel))
        db_clients = result.scalars().all()

        return [self._to_entity(db_client) for db_client in db_clients]

    def delete(self, client_id: int) -> None:
        find_client = self.session.get(ClientModel, client_id)
        self.session.delete(find_client)
        self.session.commit()

    @staticmethod
    def _to_entity(model: ClientModel) -> Client:
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