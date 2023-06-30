import logging

from json import dumps

from sqlalchemy.orm import Session

from database.engine import engine
from database.models import FieldsModel


logger = logging.getLogger(__name__)


class FieldNamesHandler:
    @staticmethod
    def save_fields(
            task_name_field: dict,
            project_field_name: dict | None,
            worker_field_name: dict | None,
            deadline_field_name: dict | None
    ):
        logger.info(
            "Saving fields {}, {}, {}, {}".format(
                task_name_field,
                project_field_name,
                worker_field_name,
                deadline_field_name
            )
        )
        with Session(bind=engine) as session:
            fields = FieldsModel(
                task_name_field=dumps(task_name_field),
                project_field_name=dumps(project_field_name) if project_field_name is not None else None,
                worker_field_name=dumps(worker_field_name) if worker_field_name is not None else None,
                deadline_field_name=dumps(deadline_field_name) if deadline_field_name is not None else None
            )

            session.add(fields)
            session.commit()

            return fields.id

    @staticmethod
    def get_fields(fields_id: int) -> dict:
        logger.info("Retrieving fields with id: {}".format(fields_id))
        with Session(bind=engine) as session:
            fields = session.query(FieldsModel).where(FieldsModel.id == fields_id).first()

            task_name = fields.task_name_field
            project = fields.project_field_name
            worker = fields.worker_field_name
            deadline = fields.deadline_field_name

            return {
                "task_name_field": task_name,
                "project_field_name": project,
                "worker_field_name": worker,
                "deadline_field_name": deadline
            }
