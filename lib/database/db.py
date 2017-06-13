import mysql.connector

class DB(object):


    def __init__(self, settings):
        self.settings = settings

    def get_db_connection(self):
        conn = mysql.connector.connect(
            user=self.settings['db']['username'],
            password=self.settings['db']['password'],
            host=self.settings['db']['host'],
            database=self.settings['db']['database']
        )
        return conn

    def query(self, query):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        results = ''
        try:
            cursor.execute(query)
            results = cursor.fetchall()
        except:
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

    def save(self, command, table_name, table):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        print('Table: {}').format(table_name)
        if type(table) is list:
            for x in table:
                cursor.execute(command, tuple(x))
        elif type(table) is dict:
            for x in table.items():
                cursor.execute(command, x)
        conn.commit()
        cursor.close()
        conn.close()

    def populate_mysql(self,
            site_table,
            header_name_table,
            header_value_table,
            header_table
        ):
        self.clear_database()
        print('Populating database...')
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
                header_table
            ]
        ]
        for command, table_name, table in tables:
            self.save(command, table_name, table)
