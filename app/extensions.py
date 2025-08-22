from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_pymongo import PyMongo
from redis import Redis

limiter = Limiter(key_func=get_remote_address)
mongo = PyMongo()


class RedisClient:
    def __init__(self):
        self._client = None

    def init_app(self, app):
        url = app.config.get("REDIS_URL")
        if url:
            self._client = Redis.from_url(url, decode_responses=True)

    @property
    def client(self):
        return self._client


redis_client = RedisClient()
