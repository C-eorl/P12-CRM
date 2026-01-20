from typing import List, Optional

from src.domain.entities.entities import Client


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