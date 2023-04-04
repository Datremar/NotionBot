from dataclasses import dataclass


@dataclass
class UserData:
    id: str
    user_db_id: str
    database_id: str
    task: dict

    def from_redis(self, key: str, value: dict):
        self.id = key

        self.user_db_id = value["user_db_id"]
        self.database_id = value["database_id"]
        self.task = value["task"]

    def to_redis(self):
        return {
            "key": self.id,
            "value": {
                "user_db_id": self.user_db_id,
                "database_id": self.database_id,
                "task": self.task
            }
        }
