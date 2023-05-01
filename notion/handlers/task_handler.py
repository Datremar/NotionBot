import notion_client.errors

from notion.client import client
from notion.handlers.utils.task_maker import TaskMaker


class TaskHandler:
    def __init__(self):
        self.database_id = "7a71bf0841c947e989ecc3ef090bc866"

    def has_db_connection(self) -> bool:
        try:
            client.databases.retrieve(database_id=self.database_id)
        except notion_client.errors.APIResponseError:
            return False

        return True

    def create_task(self, name: str, deadline: str, project_id=None, worker_id=None):
        return client.pages.create(
            parent={"database_id": self.database_id},
            properties=TaskMaker(
                    name=name,
                    worker_id=worker_id,
                    project_id=project_id,
                    deadline=deadline
                )
        )

    def get_task(self, task_id) -> dict:
        return client.pages.retrieve(task_id)

    def get_user(self, user_id) -> dict:
        response = client.pages.retrieve(user_id)
        data = {
            "username": response["properties"]["Name"]["title"][0]["text"]["content"]
        }
        return data

    def retrieve_db(self):
        return client.databases.retrieve(database_id=self.database_id)


if __name__ == "__main__":
    database_id = "7a71bf0841c947e989ecc3ef090bc866"
    task_id = "e51cc3c9724b4b01a16c54a1f85189a5"

    handler = TaskHandler(database_id=database_id)

    response = handler.create_task(
        name="Another Test Task",
        worker_id="83b1aa15-04c8-4a78-90ab-b5bc2def1fdc",
        project_id="5574a922-7a18-4387-86d3-4fd6cb794f24",
        deadline="2023-04-15"
    )

    # response = handler.get_task(task_id="67c494ddb4d34620abc37a0bf36f309b")

    # for key, val in response.items():
    #     print(key)
    #     print(val)
    #     print()
    #
    # for key, val in response["properties"].items():
    #     print(key)
    #     print(val)
    #     print()



