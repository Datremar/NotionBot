from typing import List, Type

from sqlalchemy.orm import Session

from database import engine
from database.models import UserModel


class UserHandler:
    def __new__(cls, *args, **kwargs):
        pass

    @staticmethod
    def create_user(username: str):
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
    def get_user(username: str) -> UserModel:
        with Session(bind=engine) as session:
            user = session.query(UserModel).where(UserModel.username == username).first()

            if not user:
                raise ValueError("User doesn't exist.")

            return user

    @staticmethod
    def get_all_users() -> List[Type[UserModel]]:
        with Session(bind=engine) as session:
            query = session.query(UserModel).all()

            return [user for user in query]

    @staticmethod
    def user_exists(username: str) -> bool:
        with Session(bind=engine) as session:
            return session.query(UserModel).where(UserModel.username == username).first() is not None


if __name__ == "__main__":
    pass
    # username = "TestUsername"
    # # UserHandler.create_user(username=username)
    # print(UserHandler.get_user(username=username))
    # print(UserHandler.user_exists(username=username))
    # print()
    # print(UserHandler.get_all_users())


