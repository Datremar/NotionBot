from notion.client import client


class UserHandler:
    def __init__(self, user_db_id):
        self.users = set()
        self.user_db_id = user_db_id

        users = client.databases.query(database_id=self.user_db_id)["results"]

        for user in users:
            self.users.add(user["properties"]["Name"]["title"][0]["text"]["content"])

    def get_users(self) -> set:
        return self.users

    def check_user_exists(self, username) -> bool:
        pass


if __name__ == "__main__":
    handler = UserHandler(user_db_id="941708d54a134a4181f5709e75807cd2")
    print(handler.get_users())
