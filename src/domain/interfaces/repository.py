from typing import Protocol, List, Optional

from src.domain.entities.entities import Client, User, Contrat, Event
from src.domain.entities.enums import Role


class ClientRepository(Protocol):
    """
    Client interface
    - save : Save a client
    - find_by_id : Find a client by id
    - find_all : Find all clients
    - delete : Delete a client
    """
    def save(self, client: Client) -> Client: ...

    def find_by_id(self, client_id: int) -> Optional[Client]: ...

    def find_all(self) -> List[Client]: ...

    def delete(self, client_id: int) -> None: ...


class UserRepository(Protocol):
    """
    User interface
    - save : Save a user
    - find_by_id : Find a user
    - find_all : Find all users
    - find_by_email : Find a user by email
    - find_by_role : Find a user by role
    - delete : Delete a user
    """
    def save(self, user: User) -> User: ...

    def find_by_id(self, user_id: int) -> Optional[User]: ...

    def find_all(self) -> List[User]: ...

    def find_by_email(self, email: str) -> User: ...

    def find_by_role(self, role: Role) -> List[User]: ...

    def delete(self, user_id: int) -> None: ...


class ContratRepository(Protocol):
    """
    Contrat interface
    - save : Save a contrat
    - find_by_id : Find a contrat
    - find_all : Find all contrats
    - find_by_commercial_contact : Find a contrat for commercial contact
    - find_by_client_id : Find a contrat for client id
    - find_unsigned : Find a contrat for unsigned
    - delete : Delete a contrat
    """
    def save(self, contrat) -> Contrat: ...

    def find_by_id(self, contrat_id: int) -> Contrat: ...

    def find_all(self) -> List[Contrat]: ...

    def find_by_commercial_contact(self, commercial_contact_id: int) -> List[Contrat]: ...

    def find_by_client_id(self, client_id: int) -> List[Contrat]: ...

    def find_unsigned(self) -> List[Contrat]: ...

    def delete(self, contrat_id: int) -> None: ...


class EventRepository(Protocol):
    """
    Event interface
    - save : Save an event
    - find_by_id : Find an event
    - find_all : Find all events
    - find_by_contrat : Find an event for contrat
    - find_by_support_contact : Find an event for support contact
    - find_by_client: Find an event for client
    - delete : Delete an event
    """
    def save(self, event) -> Event: ...

    def find_by_id(self, event_id: int) -> Event: ...

    def find_all(self) -> List[Event]: ...

    def find_by_contrat_id(self, contrat_id: int) -> List[Event]: ...

    def find_by_support_contact_id(self, user_id: int) -> List[Event]: ...

    def find_by_client(self, client_id: int) -> List[Event]: ...

    def delete(self, event_id: int) -> None: ...
