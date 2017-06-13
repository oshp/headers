#!/usr/bin/env python

import gevent
import argparse
from gevent import monkey; monkey.patch_all()
from lib.database.db import DB
from lib.utils.util import Util
from lib.scanner.scan import Scan

import os

from lib.utils.config import DEFAULT_CONFIG_FILE

class Headers(object):


    def __init__(self):
        self.site_table = []
        self.header_name_table = {}
        self.header_value_table = {}
        self.header_table = []
        self.headers_counter = {'name': 0, 'value': 0}
        self.config = Util()
        self.settings = self.config.load_config(DEFAULT_CONFIG_FILE)
        self.scanner = Scan(self.settings)
        self.load_header_name_table()

    def load_header_name_table(self):
        for header_name in self.settings['headers']:
            self.test_duplicate_value(
                header_name,
                self.header_name_table,
                'name')

    def work_headers(self, item):
        site_id = item[0]
        site = item[1]
        url, code, headers = self.scanner.get_data(site)
        self.site_table.append([site_id, site, url, code])
        if code > 0:
            for header_name, header_value in headers:
                if header_name in self.header_name_table:
                    hvalue = self.test_duplicate_value(
                        header_value,
                        self.header_value_table,
                        'value')
                    self.header_table.append(
                        [site_id,
                        self.header_name_table[header_name],
                        hvalue])

    def test_duplicate_value(self, value, table, index_name):
        if value not in table:
            self.headers_counter[index_name] += 1
            table[value] = self.headers_counter[index_name]
            return self.headers_counter[index_name]
        else:
            return table[value]

    def save_data(self):
        database = DB(self.settings)
        database.populate_mysql(self.site_table, self.header_name_table, self.header_value_table, self.header_table)

    def download_latest_file(self, url):
        print "[*] downloading latest topsites file"
        self.scanner.download_file(url)
        return self.settings['general']['topsites_filename']

    def main(self):
        parser = argparse.ArgumentParser(
            description='Headers will get all response headers from Alexa top sites.'
        )
        parser.add_argument(
            '-f',
            '--filename',
            default=self.settings['general']['topsites_filename'],
            help='Filename with list of sites.'
        )
        parser.add_argument(
            '-t',
            '--threads',
            type=int,
            default=self.settings['general']['thread_number'],
            help='Number of threads to make parallel request.'
        )
        #test
        parser.add_argument(
            '-d',
            '--download',
            default="https://dl.dropboxusercontent.com/u/6427240/oshp/topsites_global.csv",
            help='Download latest topsites file.'
        )
        args = parser.parse_args()

        #test
        filename = self.download_latest_file(args.download)
        #filename = args.filename
        num_threads = args.threads
        dictsites = self.config.get_dictsites(filename)
        sites = len(dictsites)
        start = 0
        thread = 1
        while (start < sites):
            print('Thread pool {} ({} - {})'.format(thread, start, start + num_threads))
            thread += 1
            threads = [gevent.spawn(self.work_headers, item) for item in dictsites[start:start+num_threads]]
            gevent.joinall(threads)
            start += num_threads
        self.scanner.get_summary(self.site_table)
        self.save_data()
