import logging

from notion.client import NotionClient


logger = logging.getLogger(__name__)


class FieldsHandler:
    def __init__(self, client: NotionClient, database_id: str):
        self.client = client
        self.database_id = database_id

    @property
    def fields(self):
        logger.info("Requesting fields from Notion")
        response = self.client.databases.retrieve(database_id=self.database_id)["properties"]
        fields = dict()

        for key, val in response.items():
            fields[key] = val

        return fields
