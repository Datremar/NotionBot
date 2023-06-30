from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)

    def __repr__(self):
        return f"{self.id}, {self.username}"


class FieldsModel(Base):
    __tablename__ = "Fields"

    id: Mapped[int] = mapped_column(primary_key=True)

    task_name_field: Mapped[str] = mapped_column(nullable=False)
    project_field_name: Mapped[str] = mapped_column(default=None, nullable=True)
    worker_field_name: Mapped[str] = mapped_column(default=None, nullable=True)
    deadline_field_name: Mapped[str] = mapped_column(default=None, nullable=True)


class ConnectionModel(Base):
    __tablename__ = "Connection"

    id: Mapped[int] = mapped_column(primary_key=True)

    user: Mapped[int] = mapped_column(ForeignKey("User.id"), nullable=False)

    name: Mapped[str] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(nullable=False)
    database_id: Mapped[str] = mapped_column(nullable=False)
    user_db_id: Mapped[str] = mapped_column(default=None, nullable=True)
    projects_db_id: Mapped[str] = mapped_column(default=None, nullable=True)
    fields: Mapped[int] = mapped_column(ForeignKey("Fields.id"), nullable=False)

    def __repr__(self):
        return f"({self.id}, {self.user}, {self.name})"
