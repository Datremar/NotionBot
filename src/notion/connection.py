import logging
from json import dumps
from typing import Tuple

from src.notion.client import NotionClient
from src.notion.handlers.projects_handler import ProjectsHandler
from src.notion.handlers.task_handler import TaskHandler
from src.notion.handlers.utils.field_names import FieldNames
from src.notion.handlers.utils.task_maker import TaskMaker
from src.notion.handlers.worker_handler import WorkerHandler

logger = logging.getLogger(__name__)


class Connection:
    def __init__(
            self,
            username: str,
            name: str,
            token: str,
            database_id: str,
            user_db_id: str | None,
            projects_db_id: str | None,
            field_names: FieldNames,
    ):
        self.username = username
        self.name = name
        self.token = token
        self.database_id = database_id
        self.user_db_id = user_db_id
        self.projects_db_id = projects_db_id
        self.field_names = field_names

        self.client = NotionClient(token=token)

        self.task_handler = TaskHandler(
            client=self.client,
            task_maker=TaskMaker(field_names=field_names),
            database_id=database_id
        )

        self.worker_handler = WorkerHandler(
            user_db_id=user_db_id,
            client=self.client
        ) if user_db_id is not None else None

        self.projects_handler = ProjectsHandler(
            projects_db_id=projects_db_id,
            client=self.client
        ) if projects_db_id is not None else None

    def has_optional_fields(self):
        return {
            "has_project": self.field_names["project_field_name"] is not None,
            "has_worker": self.field_names["worker_field_name"] is not None,
            "has_deadline": self.field_names["deadline_field_name"] is not None,
        }

    def check_connection(self) -> Tuple[bool, bool, bool]:
        logger.info("Checking databases' connections")
        return (
            self.task_handler.has_db_connection(),
            self.worker_handler.has_db_connection() if self.worker_handler is not None else True,
            self.projects_handler.has_db_connection() if self.projects_handler is not None else True,
        )

    def make_test_task(self) -> bool:
        logger.info("Making mock task")
        response = self.task_handler.create_task(
            name="TEST1"
        )

        if response is not None:
            task_id = response["id"]
            self.task_handler.delete_task(task_id=task_id)

        return response is not None

    def __json__(self, dumped=False):
        json = {
            "name": self.name,
            "token": self.token,
            "database_id": self.database_id,
            "fields": self.field_names.__json__()
        }
        if dumped:
            return dumps(json)

        return json
