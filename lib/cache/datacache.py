import redis
import json

class Datacache(object):


    def __init__(self, settings):
        self.r = redis.StrictRedis(
            host=settings['redis']['host'],
            port=settings['redis']['port'],
            db=settings['redis']['db'])

    def check_cache(self, hkey):
        return self.r.exists(hkey)

    def add_in_cache(self, hkey, data):
        self.r.set(hkey, json.dumps(data))
        self.r.expire(hkey, 86400)

    def get_data_cache(self, hkey):
        data = self.r.get(hkey)
        return json.loads(data)
