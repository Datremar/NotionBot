from notion.client import client


class _ProjectsHandler:
    def __init__(self):
        self.projects_db_id = "3510130d332640ec982bbfe8520b9b7f"
        self.projects = dict()

    def get_id(self, item):
        return self.projects[item]

    def get_projects(self) -> dict:
        response = client.databases.query(database_id=self.projects_db_id)["results"]
        self.projects = {}

        for item in response:
            name = item["properties"]["wb"]["title"][0]["plain_text"]
            id = item["id"]
            self.projects[name] = id

        return self.projects


class ProjectsHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not ProjectsHandler._instance:
            ProjectsHandler._instance = _ProjectsHandler()

        return ProjectsHandler._instance


if __name__ == "__main__":
    handler = ProjectsHandler()

    response = handler.get_projects()
    print(response)

    # for item in response:
    #     print(item)
    #     print()
