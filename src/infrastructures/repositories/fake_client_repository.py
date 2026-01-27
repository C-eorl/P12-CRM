from typing import List, Optional

from src.domain.entities.entities import Client, User, Contrat, Event
from src.domain.entities.enums import Role


class FakeClientRepository:
    def __init__(self):
        self.clients: dict[int, Client] = {}
        self._id_counter = 1

    def save(self, client: Client) -> Client:

        if client.id is None:
            # nouveau client
            client.id = self._id_counter
            self._id_counter += 1
            self.clients[client.id] = client
            return client

        if client.id in self.clients:
            # modification client
            data_client = self.clients.get(client.id)
            if data_client:
                data_client.fullname = client.fullname
                data_client.email = client.email
                data_client.telephone = client.telephone
                data_client.company_name = client.company_name
                return client


    def find_by_id(self, client_id: int) -> Optional[Client]:
        return self.clients.get(client_id)

    def find_all(self) -> List[Client]:
        return list(self.clients.values())

    def delete(self, client_id: int) -> None:
        self.clients.pop(client_id, None)



class FakeUserRepository:
    def __init__(self):
        self.users: dict[int, User] = {}
        self._id_counter = 1

    def save(self, user: User) -> User:
        if user.id is None:
            user.id = self._id_counter
            self._id_counter += 1
            self.users[user.id] = user
            return user

        if user.id in self.users:
            data_user = self.users[user.id]
            data_user.fullname = user.fullname
            data_user.email = user.email
            data_user.password = user.password
            data_user.role = user.role
            data_user.updated_at = user.updated_at
            return data_user


    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def find_all(self) -> List[User]:
        return list(self.users.values())

    def find_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if str(user.email) == email:
                return user
        return None

    def find_by_role(self, role: Role) -> List[User]:
        return [user for user in self.users.values() if user.role == role]

    def delete(self, user_id: int) -> None:
        self.users.pop(user_id, None)



class FakeContratRepository:
    def __init__(self):
        self.contrats: dict[int, Contrat] = {}
        self._id_counter = 1

    def save(self, contrat: Contrat) -> Contrat:
        if contrat.id is None:
            contrat.id = self._id_counter
            self._id_counter += 1
            self.contrats[contrat.id] = contrat
            return contrat

        if contrat.id in self.contrats:
            data_contrat = self.contrats[contrat.id]
            data_contrat.client_id = contrat.client_id
            data_contrat.commercial_contact_id = contrat.commercial_contact_id
            data_contrat.contrat_amount = contrat.contrat_amount
            data_contrat.balance_due = contrat.balance_due
            data_contrat.status = contrat.status
            data_contrat.updated_at = contrat.updated_at
            return data_contrat


    def find_by_id(self, contrat_id: int) -> Optional[Contrat]:
        return self.contrats.get(contrat_id)

    def find_all(self) -> List[Contrat]:
        return list(self.contrats.values())

    def find_by_client_id(self, client_id: int) -> List[Contrat]:
        return [
            contrat for contrat in self.contrats.values()
            if contrat.client_id == client_id
        ]

    def find_by_commercial_contact(self, commercial_contact_id: int) -> List[Contrat]:
        return [
            contrat for contrat in self.contrats.values()
            if contrat.commercial_contact_id == commercial_contact_id
        ]

    def delete(self, contrat_id: int) -> None:
        self.contrats.pop(contrat_id, None)



class FakeEventRepository:
    def __init__(self):
        self.events: dict[int, Event] = {}
        self._id_counter = 1

    def save(self, event: Event) -> Event:
        if event.id is None:
            event.id = self._id_counter
            self._id_counter += 1
            self.events[event.id] = event
            return event

        if event.id in self.events:
            data_event = self.events[event.id]
            data_event.name = event.name
            data_event.contrat_id = event.contrat_id
            data_event.client_id = event.client_id
            data_event.support_contact_id = event.support_contact_id
            data_event.start_date = event.start_date
            data_event.end_date = event.end_date
            data_event.location = event.location
            data_event.attendees = event.attendees
            data_event.notes = event.notes
            data_event.updated_at = event.updated_at
            return data_event


    def find_by_id(self, event_id: int) -> Optional[Event]:
        return self.events.get(event_id)

    def find_all(self) -> List[Event]:
        return list(self.events.values())

    def find_by_contrat_id(self, contrat_id: int) -> List[Event]:
        return [
            event for event in self.events.values()
            if event.contrat_id == contrat_id
        ]

    def find_by_client_id(self, client_id: int) -> List[Event]:
        return [
            event for event in self.events.values()
            if event.client_id == client_id
        ]

    def find_by_support_contact_id(self, support_contact_id: int) -> List[Event]:
        return [
            event for event in self.events.values()
            if event.support_contact_id == support_contact_id
        ]

    def delete(self, event_id: int) -> None:
        self.events.pop(event_id, None)
