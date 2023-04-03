import datetime

from notion.client import client
from notion.handlers.utils.task_maker import TaskMaker


class TaskHandler:
    def __init__(self, database_id):
        self.database_id = database_id

    def create_task(self, name: str, text: str, description: str, worker: str, deadline: str):
        task = TaskMaker(
            name=name,
            text=text,
            description=description,
            worker=worker,
            deadline=deadline
        )

        return client.pages.create(parent={"database_id": self.database_id}, properties=task)

    def get_task(self, task_id) -> dict:
        return client.pages.retrieve(task_id)

    def get_user(self, user_id) -> dict:
        response = client.pages.retrieve(user_id)
        data = {
            "username": response["properties"]["Name"]["title"][0]["text"]["content"]
        }
        return data


if __name__ == "__main__":
    user_db_id = "941708d54a134a4181f5709e75807cd2"
    database_id = "5f4ae22fb2f54e2fb172a55e549467be"

    handler = TaskHandler(database_id=database_id)

    response = handler.create_task(
        name="Boink",
        text="Something?",
        description="Well, do something!~",
        worker=handler.get_user(user_id="ca97cb16adba496daf58e981680092c3")["username"],
        deadline=(datetime.date.today() + datetime.timedelta(days=3)).__str__()
    )

    for key, value in response["properties"].items():
        print(key + ":")
        print(value)
        print()

    # print(handler.get_user(user_id="ca97cb16adba496daf58e981680092c3"))

    # response = handler.get_task(task_id="b5d2210e9b5c4c48b078be9b59b8af9f")["properties"]
    #
    # for key, value in response.items():
    #     print(key + ":")
    #     print(value)
    #     print()
