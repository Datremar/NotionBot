from dataclasses import dataclass


@dataclass
class UserData:
    username: str
    task: dict
    deadline: dict

    def wipe(self):
        self.task.clear()
        self.deadline.clear()

    def to_dict(self):
        return self.username, {
            "task": self.task,
        }


if __name__ == "__main__":
    u1 = UserData(
        username="Datremar",
        task={},
        deadline={}
    )

    print(u1)
    print(*u1.to_dict())
