import json
from typing import Union

import redis

from json import dumps, loads

from tg_bot.utils.user_data import UserData


class _RedisClient:
    def __init__(self, host: str, port: int):
        self.pool = redis.ConnectionPool(host=host, port=port, db=0)
        self.redis = None

    def init(self):
        self.redis = redis.Redis(connection_pool=self.pool)

    def save_user(self, user: UserData):
        self.__setitem__(user.id, user.to_redis())

    def __getitem__(self, key: str):
        if type(key) is not str:
            raise TypeError("The key provided was not str type.")

        value = self.redis.get(key)

        try:
            return loads(value)
        except json.JSONDecodeError:
            return value

    def __setitem__(self, key: str, value: Union[str, dict]):
        if type(key) is not str:
            raise TypeError("The key provided was not str type.")

        if type(value) not in [str, dict]:
            raise TypeError("The value provided was not str or dict type.")

        if type(value) is dict:
            self.redis.set(key, dumps(value))


class RedisClient:
    _instance = None

    def __new__(cls):
        if not RedisClient._instance:
            RedisClient._instance = _RedisClient(host="localhost", port=6379)

        return RedisClient._instance
