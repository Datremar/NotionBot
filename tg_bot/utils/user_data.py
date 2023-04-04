from dataclasses import dataclass


@dataclass
class UserData:
    id: str
    user_db_id: str
    database_id: str
    task: dict

    def to_redis(self):
        return {
            "key": self.id,
            "value": {
                "user_db_id": self.user_db_id,
                "database_id": self.database_id,
                "task": self.task
            }
        }
