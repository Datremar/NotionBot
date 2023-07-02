from dataclasses import dataclass
from typing import Dict

from notion.connection import Connection


@dataclass
class UserData:
    username: str
    connections: Dict[str, Connection]
    current_connection: Connection | None
