from notion_client import Client


class NotionClient(Client):
    def __init__(self, *args, token: str, **kwargs):
        super().__init__(*args, auth=token, **kwargs)
        self.token = token

    def __repr__(self):
        return {"token": self.token}.__str__()

    def __str__(self):
        return {"token": self.token}.__str__()
