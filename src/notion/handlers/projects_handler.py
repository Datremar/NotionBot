import logging

from notion_client import APIResponseError

from src.notion.client import NotionClient


logger = logging.getLogger(__name__)


class ProjectsHandler:
    def __init__(self, projects_db_id: str, client: NotionClient):
        self.client = client
        self.projects_db_id = projects_db_id
        self.projects = dict()

    def has_db_connection(self) -> bool:
        logger.info("Checking Notion db connection")
        try:
            self.client.databases.retrieve(database_id=self.projects_db_id)
        except APIResponseError:
            return False

        return True

    def get_id(self, item):
        if item not in self.projects:
            return None
        return self.projects[item]

    def get_projects(self) -> dict:
        logger.info("Requesting projects from Notion projects db")
        response = self.client.databases.query(database_id=self.projects_db_id)["results"]
        self.projects = {}

        for item in response:
            name = item["properties"]["wb"]["title"][0]["plain_text"]
            id = item["id"]
            self.projects[name] = id

        return self.projects
