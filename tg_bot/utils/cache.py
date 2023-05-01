from tg_bot.utils.data_models import UserData


class _Cache:
    def __init__(self):
        self.cache = dict()

    def __getitem__(self, item: str) -> UserData:
        return self.cache[item]

    def __setitem__(self, key: str, value: UserData):
        self.cache[key] = value

    def __contains__(self, item):
        return item in self.cache


cache = _Cache()
