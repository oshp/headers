import redis
import json
import os

from lib.utils.util import load_env_config


class Datacache():

    def __init__(self):
        load_env_config()

        self.r = redis.StrictRedis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            db=os.getenv("REDIS_DB"))

    def check_cache(self, hkey):
        return self.r.exists(hkey)

    def add_in_cache(self, hkey, data):
        self.r.set(hkey, json.dumps(data))
        self.r.expire(hkey, os.getenv("REDIS_TTL"))

    def get_data_cache(self, hkey):
        data = self.r.get(hkey)
        return json.loads(data)
