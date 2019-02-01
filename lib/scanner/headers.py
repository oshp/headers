# coding: utf-8
import os
import gevent

from gevent import monkey; monkey.patch_all()

from lib.utils.util import get_dictsites
from lib.utils.util import load_env_config

from lib.database.rdms_db import MySQL
from lib.scanner.scan import Scan
from lib.secureheaders.site import Site

class Headers():

    def __init__(self):
        load_env_config()
        self.headers_filter = os.getenv('HEADERS').lower().split(',')
        self.scanner = Scan()
        self.data = []

    def work_headers(self, topsites_row):
        try:
            site = Site({'id': topsites_row[0], 'domain': topsites_row[1]})
            response = self.scanner.connect(site['domain'])
            if response  or (response['status_code' == 200]):
                site.update({'url': response['url']})
                site.update({'status_code': response['status_code']})
                for header in response['headers'].keys():
                    if header in self.headers_filter:
                        site['headers'].update({header: response['headers'][header]})
            self.data.append(site)
        except TypeError:
            print("[!] site <{}> will be excluded from the analysis".format(topsites_row[1]))

    def save_data(self):
        database = MySQL()
        database.populate_mysql(self.data)

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
        self.scanner.get_summary(self.data)
        self.save_data()