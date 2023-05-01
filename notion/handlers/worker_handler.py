from notion.client import client


class _WorkerHandler:
    def __init__(self):
        self.user_db_id = "7bd724339e9141899b09ee2ca4547df6"
        self.workers = dict()

    def get_id(self, item):
        return self.workers[item]

    def get_workers(self) -> dict:
        response = client.databases.query(database_id=self.user_db_id)["results"]
        self.workers = {}

        for item in response:
            name = item["properties"]["Имя"]["title"][0]["plain_text"]
            id = item["id"]
            self.workers[name] = id

        return self.workers


class WorkerHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not WorkerHandler._instance:
            WorkerHandler._instance = _WorkerHandler()

        return WorkerHandler._instance


if __name__ == "__main__":
    handler = WorkerHandler()
    response = handler.get_workers()

    print(response)

    print()
    print()
    print()

    print(client.pages.retrieve("83b1aa15-04c8-4a78-90ab-b5bc2def1fdc"))

    # for item in response:
    #     print(item["properties"]["Имя"]["title"][0]["plain_text"])
    #     print(item["id"])
    #     print()
