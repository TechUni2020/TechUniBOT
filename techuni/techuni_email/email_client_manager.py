import os
from yaml import safe_load
from techuni.util import multi_dirname
from techuni.techuni_email import EmailClient

class EmailClientManager:
    _FOLDER = os.path.join(multi_dirname(__file__, 3), "email_clients")

    def __init__(self):
        self.clients: dict[str, EmailClient] = {}
        for file in os.listdir(self._FOLDER):
            with open(os.path.join(self._FOLDER, file), "r") as f:
                data: dict = safe_load(f)
            if "TEST" in data:
                continue
            client = EmailClient(data)
            self.clients[client.address] = client

    def get(self, address: str) -> EmailClient:
        if address not in self.clients:
            raise KeyError(f"Client {address} is not found")
        return self.clients[address]

    def __getitem__(self, item):
        return self.get(item)

    def __iter__(self):
        return iter(self.clients.items())

    def __len__(self):
        return len(self.clients)

    def __contains__(self, item):
        return item in self.clients
