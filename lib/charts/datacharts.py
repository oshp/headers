# coding: utf-8
from lib.database.rdms_db import MySQL
from lib.database.memory_db import Redis

from lib.secureheaders.sites import Sites


class Datacharts():

    def __init__(self):
        self.db = MySQL()
        self.cache = Redis()

    def make_query(self, data):
        return {key: self.db.query(query)[0][0] for key, query in data.items()}

    def get_datachart(self, key, data):
        datachart = {}
        if self.cache.check_cache(key):
            datachart = self.cache.get_data_cache(key)
        else:
            datachart = self.make_query(data)
            self.cache.add_in_cache(key, datachart)
        return datachart

    def get_total_sites(self):
        sites = Sites()
        return self.get_datachart(sites.sites, sites.options)
