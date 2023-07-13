import logging

from sqlalchemy.orm import Session

from src.database.engine import engine
from src.database.models import UserModel, ConnectionModel, FieldsModel


logger = logging.getLogger(__name__)


class ConnectionHandler:
    def __new__(cls, *args, **kwargs):
        pass

    @staticmethod
    def save_connection(
            username: str,
            name: str,
            token: str,
            database_id: str,
            user_db_id: str | None,
            projects_db_id: str | None,
            fields: dict
    ):
        logger.info("{} is saving connection {}".format(username, name))
        with Session(bind=engine) as session:
            user = session.query(UserModel).where(UserModel.username == username).first()

            fields = FieldsModel(
                task_name_field=fields["task_name_field"],
                project_field_name=fields["project_field_name"],
                worker_field_name=fields["worker_field_name"],
                deadline_field_name=fields["deadline_field_name"]
            )

            session.add(fields)
            session.commit()

            connection = ConnectionModel(
                user=user.id,
                name=name,
                token=token,
                database_id=database_id,
                user_db_id=user_db_id,
                projects_db_id=projects_db_id,
                fields=fields.id
            )

            session.add(connection)
            session.commit()

    @staticmethod
    def get_user_connections(username: str) -> tuple:
        logger.info("Retrieving {}'s connections".format(username))
        with Session(bind=engine) as session:

            user = session.query(UserModel).where(UserModel.username == username).first()
            connections = session.query(ConnectionModel) \
                .where(ConnectionModel.user == user.id).all()

            return tuple(connection for connection in connections)

    @staticmethod
    def delete_connection(username: str, name: str):
        logger.info("{} is deleting connection".format(username))
        with Session(bind=engine) as session:
            user = session.query(UserModel).where(UserModel.username == username).first()
            connection = session.query(ConnectionModel) \
                .where(ConnectionModel.user == user.id) \
                .where(ConnectionModel.name == name).first()

            session.delete(connection)
            session.commit()
