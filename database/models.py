from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return rf"User(id={self.id}, username={self.username})"


class NotionLinkModel(Base):
    __tablename__ = "NotionLink"

    id = Column(Integer, primary_key=True)
    database_id = Column(String, nullable=False)
    user_db_id = Column(String, nullable=False)
    projects_db_id = Column(String, nullable=False)

    user = Column(Integer, ForeignKey("User.id"))

    def __repr__(self):
        return f"Link(id={self.id}, user={self.user}, database_id={self.database_id}, user_db_id={self.user_db_id}, projects_db_id={self.projects_db_id})"

