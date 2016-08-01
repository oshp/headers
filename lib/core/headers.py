#!/usr/bin/env python

import gevent
import argparse
from gevent import monkey; monkey.patch_all()
import db
import util
import scan

site_table = []
header_name_table = []
header_name_table_inverted = {}
header_value_table = []
header_value_table_inverted = {}
header_table = []
header_name_id = 0
header_value_id = 0
header_id = 0

class Headers:

    def __init__(self):
        global settings, database, config, scanner
        config = util.Util()
        settings = config.load_config()
        scanner = scan.Scan(settings)
        database = db.DB(settings)

    def work_headers(self, item):
        global site_table, header_name_table, header_name_table_inverted, header_value_table, header_value_table_inverted, header_table, header_name_id, header_value_id, header_id
        site_id = item[0]
        site = item[1]
        url, code, headers = scanner.get_data(site)
        site_table.append([site_id, site, url, code])
        if code > 0:
            for header_name, header_value in headers:
                header_id += 1
                if header_name not in header_name_table:
                    header_name_id += 1
                    header_name_table.append(header_name)
                    header_name_table_inverted[header_name] = header_name_id
                    actual_header_name_id = header_name_id
                else:
                    actual_header_name_id = header_name_table_inverted[header_name]
                if header_value not in header_value_table:
                    header_value_id += 1
                    header_value_table.append(header_value)
                    header_value_table_inverted[header_value] = header_value_id
                    actual_header_value_id = header_value_id
                else:
                    actual_header_value_id = header_value_table_inverted[header_value]
                header_table.append([header_id, site_id, actual_header_name_id, actual_header_value_id])

    def main(self):
        parser = argparse.ArgumentParser(
            description='Headers will get all response headers from Alexa top sites.'
        )
        parser.add_argument(
            '-f',
            '--filename',
            default=settings['general']['topsites_filename'],
            help='Filename with list of sites.'
        )
        parser.add_argument(
            '-t',
            '--threads',
            type=int,
            default=settings['general']['thread_number'],
            help='Number of threads to make parallel request.'
        )
        args = parser.parse_args()

        filename = args.filename
        num_threads = args.threads
        dictsites = config.get_dictsites(filename)
        sites = len(dictsites)
        start = 0
        thread = 1
        while (start < sites):
            print 'Thread pool {} ({} - {})'.format(thread, start, start + num_threads)
            thread += 1
            threads = [gevent.spawn(self.work_headers, item) for item in dictsites[start:start+num_threads]]
            gevent.joinall(threads)
            start += num_threads
        scanner.get_summary()
        database.populate_mysql(site_table, header_name_table, header_value_table, header_table)
