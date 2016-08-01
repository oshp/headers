import mysql.connector

conn = None

class DB:

    def __init__(self, settings):
        self.settings = settings

    def get_db_connection(self):
        global conn
        if conn == None:
            conn = mysql.connector.connect(
                user=self.settings['db']['username'],
                password=self.settings['db']['password'],
                host=self.settings['db']['host'],
                database=self.settings['db']['database']
            )
        return conn

    def close_db_connection(self):
        conn = self.get_db_connection()
        conn.close()

    def clear_database(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        print '\nCleaning database'
        print 'Tables: [header, site, header_value, header_name]'
        print ''
        db_tables = [
            'DELETE FROM headers.header WHERE header_id>0;',
            'DELETE FROM headers.site WHERE site_id>0;',
            'DELETE FROM headers.header_value WHERE header_value_id>0;',
            'DELETE FROM headers.header_name WHERE header_name_id>0;'
        ]
        for command in db_tables:
            cursor.execute(command)
        conn.commit()
        cursor.close()

    def save_header_value_table(self, header_value_table):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        print 'Table: header_value'
        for value in header_value_table:
            header_value_id = header_value_table.index(value) + 1
            cursor.execute(
                'INSERT INTO \
                `headers`.`header_value` \
                (`header_value_id`, `value`) \
                VALUES \
                (%s, %s)',
                (header_value_id, value))
        conn.commit()
        cursor.close()

    def save_header_name_table(self, header_name_table):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        print 'Table: header_name'
        for name in header_name_table:
            header_name_id = header_name_table.index(name) + 1
            cursor.execute(
                'INSERT INTO \
                `headers`.`header_name` \
                (`header_name_id`, `name`) \
                VALUES \
                (%s, %s)',
                (header_name_id, name))
        conn.commit()
        cursor.close()

    def save_header_table(self, header_table):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        print 'Table: header'
        for header_id, site_id, header_name_id, header_value_id in header_table:
            cursor.execute(
            'INSERT INTO \
            `headers`.`header` \
            (`header_id`, `site_id`, `header_name_id`, `header_value_id`) \
            VALUES \
            (%s, %s, %s, %s)',
            (header_id, site_id, header_name_id, header_value_id))
        conn.commit()
        cursor.close()

    def save_site_table(self, site_table):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        print 'Table: site'
        for site_id, site, url, code in site_table:
            cursor.execute(
                'INSERT INTO \
                `headers`.`site` (`site_id`, `site`, `url`, `code`) \
                VALUES \
                (%s, %s, %s, %s)',
                (site_id, site, url, code))
        conn.commit()
        cursor.close()

    def populate_mysql(self,
            site_table,
            header_name_table,
            header_value_table,
            header_table
        ):
        self.clear_database()
        print 'Populating MySQL tables'
        self.save_site_table(site_table)
        self.save_header_value_table(header_value_table)
        self.save_header_name_table(header_name_table)
        self.save_header_table(header_table)
        self.close_db_connection()
