import logging
from typing import List, Type

from sqlalchemy.orm import Session

from src.database.engine import engine
from src.database.models import UserModel


logger = logging.getLogger(__name__)


class UserHandler:
    def __new__(cls, *args, **kwargs):
        pass

    @staticmethod
    def save_user(username: str):
        logger.info("Saving user {}".format(username))
        with Session(bind=engine) as session:
            if not UserHandler.user_exists(username=username):
                user = UserModel(
                    username=username
                )

                session.add(user)
                session.commit()

                return user

            raise ValueError("User already exists.")

    @staticmethod
    def get_all_users() -> List[Type[UserModel]]:
        logger.info("Getting all users")
        with Session(bind=engine) as session:
            query = session.query(UserModel).all()

            return [user for user in query]

    @staticmethod
    def user_exists(username: str) -> bool:
        with Session(bind=engine) as session:
            return session.query(UserModel).where(UserModel.username == username).first() is not None
