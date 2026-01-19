from typing import List

from src.domain.entities.entities import Client


class FakeClientRepository:
    def __init__(self):
        self.clients: dict[int, Client] = {}
        self._id_counter = 1

    def save(self, client: Client) -> Client | None:

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
                data_client.fullname = client.fullname if client.fullname is not None else None
                data_client.email = client.email if client.email is not None else None
                data_client.telephone = client.telephone if client.telephone is not None else None
                data_client.company_name = client.company_name if client.company_name is not None else None
                return client

        return None

    def find_by_id(self, client_id: int) -> Client:
        return self.clients.get(client_id)

    def find_all(self) -> List[Client]:
        return list(self.clients.values())

    def delete(self, client_id: int) -> None:
        self.clients.pop(client_id, None)