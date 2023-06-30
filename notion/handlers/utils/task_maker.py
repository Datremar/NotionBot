import logging

from .field_names import FieldNames
from .fields import NameField, ProjectField, WorkerField, DeadlineField


logger = logging.getLogger(__name__)


class TaskMaker:
    def __init__(self, field_names: FieldNames):
        self.fields = field_names

    def make_request(
            self,
            name: str,
            worker_id: str | None,
            project_id: str | None,
            deadline: str | None,
    ) -> dict:
        logger.info("Constructing request to Notion")
        request = dict()

        request.__setitem__(*NameField(self.fields["task_name_field"], name))

        if project_id is not None:
            request.__setitem__(*ProjectField(self.fields["project_field_name"], project_id))
        if worker_id is not None:
            request.__setitem__(*WorkerField(self.fields["worker_field_name"], worker_id))
        if deadline is not None:
            request.__setitem__(*DeadlineField(self.fields["deadline_field_name"], deadline))

        logger.info("Request: {}".format(request))
        return request
