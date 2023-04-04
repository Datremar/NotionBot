class TaskMaker:
    def __new__(cls, name: str, description: str, worker: str, deadline: str) -> dict:
        return {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": name
                        }
                    }
                ]
            },
            "Status": {
                "select": {
                    "id": '1',
                    "name": "To Do",
                    "color": "red"
                }
            },
            "Description": {
                "rich_text": [
                    {
                        "text": {
                            "content": description
                        }
                    }
                ]
            },
            "Worker": {
                "rich_text": [
                    {
                        "text": {
                            "content": worker
                        }
                    }
                ]
            },
            "Deadline": {
                "date": {
                    "start": deadline,
                    "end": None,
                    "time_zone": None
                }
            }
        }
