# coding: utf-8
import os
import gevent

from gevent import monkey; monkey.patch_all()

from lib.utils.util import get_dictsites
from lib.utils.util import load_env_config

from lib.database.rdms_db import MySQL
from lib.scanner.scan import Scan


class Headers():

    def __init__(self):
        load_env_config()
        self.site_table = []
        self.header_name_table = {}
        self.header_value_table = {}
        self.header_table = []
        self.headers_counter = {'name': 0, 'value': 0}
        self.scanner = Scan()
        self.load_header_name_table()

    def load_header_name_table(self):
        for header_name in os.getenv('HEADERS').lower().split(','):
            self.test_duplicate_value(
                header_name,
                self.header_name_table,
                'name')

    def work_headers(self, topsites_row):
        try:
            site_id = topsites_row[0]
            site = topsites_row[1]
            response = self.scanner.connection(site)
            if response  or (response['status_code' == 200]):
                self.site_table.append([site_id, site, response['url'], response['status_code']])
                for header_name, header_value in response['headers'].items():
                    if header_name in self.header_name_table:
                        hvalue = self.test_duplicate_value(header_value,
                                                           self.header_value_table,
                                                           'value')
                        self.header_table.append([site_id,
                                                  self.header_name_table[header_name],
                                                  hvalue])
        except TypeError:
            print("[!] site <{}> will be excluded from the analysis".format(site))

    def test_duplicate_value(self, value, table, index_name):
        if value not in table:
            self.headers_counter[index_name] += 1
            table[value] = self.headers_counter[index_name]
            return self.headers_counter[index_name]
        else:
            return table[value]

    def save_data(self):
        database = MySQL()
        database.populate_mysql(self.site_table,
                                self.header_name_table,
                                self.header_value_table,
                                self.header_table)

    def run(self, filename, num_threads):
        dictsites = get_dictsites(filename)
        start = 0
        thread = 1
        while (start < len(dictsites)):
            print('Thread pool {} ({} - {})'.format(thread, start, start + num_threads))
            thread += 1
            threads = [gevent.spawn(self.work_headers, item) for item in dictsites[start:start+num_threads]]
            gevent.joinall(threads)
            start += num_threads
        self.scanner.get_summary(self.site_table)
        self.save_data()
