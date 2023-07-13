import logging

from notion_client import Client


logger = logging.getLogger(__name__)


class NotionDBHandler:
    def __init__(self, client: Client):
        self.client = client

    @property
    def databases(self):
        logger.info("Requesting databases from Notion")

        dbs = dict()

        response = self.client.search(
            **{
                "filter": {
                    "value": "database",
                    "property": "object"
                }
            }
        )["results"]

        for result in response:
            name = result["title"][0]["text"]["content"]
            db_id = result["id"]

            dbs[name] = db_id

        return dbs
