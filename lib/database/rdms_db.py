# coding: utf-8
import os
import sys
import mysql.connector

import functools

from mysql.connector.errors import Error
from mysql.connector.errors import InterfaceError

from lib.utils.util import load_env_config


class MySQL():

    def __init__(self):
        load_env_config()
        self.headers_filter = os.getenv('HEADERS').lower().split(',')

    def get_db_connection(self):
        try:
            conn = mysql.connector.connect(
                user=os.getenv("MYSQL_USERNAME"),
                password=os.getenv("MYSQL_PASSWORD"),
                host=os.getenv("MYSQL_HOST"),
                database=os.getenv("MYSQL_DATABASE")
            )
        except InterfaceError:
            print("[*] mysql server unavailable...")
            print("[>] please check if there's any server listening on: <{}:3306>".format(os.getenv('MYSQL_HOST')))
            sys.exit(1)
        return conn

    @functools.lru_cache(maxsize=64)
    def query(self, query):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        results = []
        try:
            cursor.execute(query)
            results = cursor.fetchall()
        except Error:
            print("[!] error: unable to fecth data")
        finally:
            conn.commit()
            cursor.close()
            conn.close()
        return results

    def clear_database(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        print('')
        print('Cleaning database')
        print('Tables: [header, site, header_value, header_name]')
        print('')
        db_tables = [
            'DELETE FROM header WHERE header_id>0;',
            'DELETE FROM site WHERE site_id>0;',
            'DELETE FROM header_value WHERE header_value_id>0;',
            'DELETE FROM header_name WHERE header_name_id>0;'
        ]
        for command in db_tables:
            cursor.execute(command)
        conn.commit()
        cursor.close()

    def _site_table(self, data):
        return [[site['id'], site['domain'], site['url'], site['status_code']] for site in data]

    def _header_value_table(self, data):
        count = 0
        table = {}
        for site in data:
            for header_name in site['headers'].keys():
                if header_name not in table.keys():
                    count += 1
                    table[site['headers'][header_name]] = count
        return table

    def _header_name_table(self, data):
        count = 0
        table = {}
        for site in data:
            for header_name in site['headers'].keys():
                if header_name not in table.keys():
                    count += 1
                    table[header_name] = count
        return table

    def _h_table(self, data, header_value_table, header_name_table):
        table = []
        for site in data:
            for header in site['headers'].keys():
                table.append([site['id'],
                    header_name_table[header],
                    header_value_table[site['headers'][header]]
                ])
        return table

    def populate_mysql(self, data):
        self.clear_database()
        print('Populating database...')

        site_table = self._site_table(data)
        header_value_table = self._header_value_table(data)
        header_name_table = self._header_name_table(data)
        h_table = self._h_table(data, header_value_table, header_name_table)

        tables = [
            [
                'INSERT INTO `site` (`site_id`, `site`, `url`, `code`) VALUES (%s, %s, %s, %s)',
                'site',
                site_table
            ],
            [
                'INSERT INTO `header_value` (`value`, `header_value_id`) VALUES (%s, %s)',
                'header_value',
                header_value_table
            ],
            [
                'INSERT INTO `header_name` (`name`, `header_name_id`) VALUES (%s, %s)',
                'header_name',
                header_name_table
            ],
            [
                'INSERT INTO `header` (`site_id`, `header_name_id`, `header_value_id`) VALUES (%s, %s, %s)',
                'header',
                h_table
            ]
        ]
        for command, table_name, table in tables:
            self.save(command, table_name, table)

    def save(self, command, table_name, table):
        print('Table: {}'.format(table_name))
        conn = self.get_db_connection()
        cursor = conn.cursor()
        if type(table) is list:
            for x in table:
                cursor.execute(command, tuple(x))
        elif type(table) is dict:
            for x in table.items():
                cursor.execute(command, x)
        conn.commit()
        cursor.close()
        conn.close()
