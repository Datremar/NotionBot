import logging

from database.handlers.connection_handler import ConnectionHandler
from database.handlers.field_names_handler import FieldNamesHandler
from database.handlers.user_handler import UserHandler
from notion.connection import Connection
from notion.handlers.utils.field_names import FieldNames
from tg_bot.utils.data_models import UserData


logger = logging.getLogger(__name__)


class _Cache:
    def __init__(self):
        self.cache = dict()

    def load(self):
        logger.info("Loading data to cache")
        users = UserHandler.get_all_users()

        for user in users:
            connections = {}
            models = ConnectionHandler.get_user_connections(user.username)

            for model in models:
                connection = Connection(
                    username=user.username,
                    name=model.name,
                    token=model.token,
                    database_id=model.database_id,
                    user_db_id=model.user_db_id,
                    projects_db_id=model.projects_db_id,
                    field_names=FieldNames(
                        **FieldNamesHandler.get_fields(model.fields)
                    )
                )
                connections[model.name] = connection

            profile = UserData(
                username=user.username,
                connections=connections,
                current_connection=None
            )

            cache[user.username] = {
                "profile": profile,
                "context": {
                    "connection": {},
                    "set_fields": {}
                }
            }

    def new_profile(self, username: str):
        logger.info("Cached new profile")
        user = UserData(
            username=username,
            connections={},
            current_connection=None
        )

        cache[username] = {
            "profile": user,
            "context": {
                "connection": {},
                "set_fields": {}
            }
        }

        user.save(UserHandler)

    def wipe_context(self, username: str):
        logger.info(f"Wiping {username}'s context")
        self.cache[username]["context"] = {
            "connection": {},
            "set_fields": {}
        }

    def __getitem__(self, item: str) -> UserData:
        return self.cache[item]

    def __setitem__(self, key: str, value):
        self.cache[key] = value

    def __contains__(self, item):
        return item in self.cache


cache = _Cache()
