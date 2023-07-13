import logging

from notion_client import APIResponseError

from src.notion.client import NotionClient


logger = logging.getLogger(__name__)


class WorkerHandler:
    def __init__(self, user_db_id: str, client: NotionClient):
        self.client = client
        self.user_db_id = user_db_id
        self.workers = dict()

    def has_db_connection(self) -> bool:
        logger.info("Checking db connection")
        try:
            self.client.databases.retrieve(database_id=self.user_db_id)
        except APIResponseError:
            return False

        return True

    def get_id(self, item):
        if item not in self.workers:
            return None
        return self.workers[item]

    def get_workers(self) -> dict:
        logger.info("Requesting workers from Notion db")
        response = self.client.databases.query(database_id=self.user_db_id)["results"]
        self.workers = {}

        for item in response:
            name = item["properties"]["Имя"]["title"][0]["plain_text"]
            id = item["id"]
            self.workers[name] = id

        return self.workers
