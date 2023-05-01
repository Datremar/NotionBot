from typing import List, Type

from sqlalchemy.orm import Session

from database import engine

from database.models import NotionLinkModel, UserModel


class LinkHandler:
    def __new__(cls, *args, **kwargs):
        pass

    @staticmethod
    def create_link(username: str, database_id: str, user_db_id: str, projects_db_id: str):
        with Session(bind=engine) as session:
            if not LinkHandler.link_exists(
                username=username,
                database_id=database_id,
                user_db_id=user_db_id,
                projects_db_id=projects_db_id
            ):
                link = NotionLinkModel(
                    user=session.query(UserModel).where(UserModel.username == username).first().id,
                    database_id=database_id,
                    user_db_id=user_db_id,
                    projects_db_id=projects_db_id
                )

                session.add(link)
                session.commit()

                return link

            raise ValueError("Link already exists.")

    @staticmethod
    def get_link(username: str) -> NotionLinkModel:
        with Session(bind=engine) as session:
            user = session.query(UserModel).where(UserModel.username == username).first()
            link = session.query(NotionLinkModel).where(
                NotionLinkModel.user == user.id
            ).first()

            if not link:
                raise ValueError("Link doesn't exist.")

            return link

    @staticmethod
    def get_all_links(username: str) -> List[Type[NotionLinkModel]]:
        with Session(bind=engine) as session:
            user = session.query(UserModel).where(UserModel.username == username).first()
            links = session.query(NotionLinkModel).where(NotionLinkModel.user == user.id)

            if not links:
                raise ValueError(rf"This user {username} doesn't have any links.")

            return [link for link in links]

    @staticmethod
    def link_exists(username: str, database_id: str, user_db_id: str, projects_db_id: str) -> bool:
        with Session(bind=engine) as session:
            user = session.query(UserModel).where(UserModel.username == username).first()
            return session.query(UserModel).where(
                NotionLinkModel.user == user.id,
                NotionLinkModel.database_id == database_id,
                NotionLinkModel.user_db_id == user_db_id,
                NotionLinkModel.projects_db_id == projects_db_id
            ).first() is not None


if __name__ == "__main__":
    pass
    # from database.handlers.user_handler import UserHandler
    # user = UserHandler.create_user("TestUser")
    # link = LinkHandler.create_link(
    #     username="TestUser",
    #     database_id="123",
    #     user_db_id="321",
    #     database_name="TestDB"
    # )
    #
    # link1 = LinkHandler.create_link(
    #     username="TestUser",
    #     database_id="1234",
    #     user_db_id="4321",
    #     database_name="TestDB1"
    # )
    #
    # link2 = LinkHandler.create_link(
    #     username="TestUser",
    #     database_id="123",
    #     user_db_id="321",
    #     database_name="TestDB2"
    # )
    #
    # links = LinkHandler.get_all_links("TestUser")
    #
    # for link in links:
    #     print(link)

