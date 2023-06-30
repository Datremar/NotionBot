from dataclasses import dataclass
from typing import Dict

from notion.connection import Connection


@dataclass
class UserData:
    username: str
    connections: Dict[str, Connection]
    current_connection: Connection | None

    def save(self, user_handler):
        user_handler.save_user(username=self.username)

