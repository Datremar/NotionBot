import logging

from notion_client.errors import APIResponseError

from notion.client import NotionClient
from notion.handlers.utils.task_maker import TaskMaker


logger = logging.getLogger(__name__)


class TaskHandler:
    def __init__(self, client: NotionClient, task_maker: TaskMaker, database_id: str):
        self.client = client
        self.database_id = database_id
        self.task_maker = task_maker

    def has_db_connection(self) -> bool:
        logger.info("Checking db connection")
        try:
            self.client.databases.retrieve(database_id=self.database_id)
        except APIResponseError as e:
            logger.error(e.__str__())
            return False

        return True

    def create_task(self, name: str, deadline=None, project_id=None, worker_id=None):
        logger.info("Requesting task creation")
        try:
            response = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=self.task_maker.make_request(
                    name=name,
                    worker_id=worker_id,
                    project_id=project_id,
                    deadline=deadline,
                )
            )
        except APIResponseError as e:
            logger.error(e.__str__())
            return None

        return response

    def delete_task(self, task_id: str):
        logger.info("Deleting task")
        logger.debug(
            self.client.pages.update(
                page_id=task_id,
                archived=True
            )
        )

    def __repr__(self):
        return {"id": self.database_id}.__str__()
