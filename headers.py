#!/usr/bin/python -tt

import sys
import urllib2
from urlparse import urlparse
import socket
import httplib
import gevent
from gevent import monkey; monkey.patch_all()
import mysql.connector
from mysql.connector import errorcode

__author__ = 'Ricardo Iramar dos Santos'
chttps = 0
chttp = 0
cerror = 0
site_table = {}
header_name_table = {}
header_name_table_inverted = {}
header_value_table = {}
header_value_table_inverted = {}
header_table = {}
header_name_id = 0
header_value_id = 0
header_id = 0

def connection(url):
    #proxy = urllib2.ProxyHandler({'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'})
    #opener = urllib2.build_opener(proxy)
    #urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36')
    req.add_header('Origin', 'http://a.com')
    try:
        response = urllib2.urlopen(req, timeout=3)
    except urllib2.HTTPError as error:
        return error.geturl(), error.getcode(), error.info().items()
    except urllib2.URLError as error:
        return str(error.reason), -1, ''
    except socket.error as error:
        return str(error), -2, ''
    except httplib.BadStatusLine, error:
        return str(error), -3, ''
    except httplib.HTTPException, error:
        return str(error), -4, ''
    else:
        return response.geturl(), response.getcode(), response.info().items()

def get_data(site):
    global chttps, chttp, cerror
    url = 'https://' + site
    newurl, code, headers = connection(url) # Trying HTTPS
    if code < 0:
        url = 'http://' + site
        newurl, code, headers = connection(url) # Trying HTTP
        if code < 0:
            cerror += 1
            #print 'ERROR:', url, code, newurl
            return newurl, code, ''
        else:
            if urlparse(newurl).scheme == 'https':
                chttps += 1 # HTTPS redirect OK
            else:
                chttp += 1 # HTTP OK
    else:
        if urlparse(newurl).scheme == 'http':
            chttp += 1 # HTTP redirect OK
        else:
            chttps += 1 # HTTPS OK
    return newurl, code, headers

def work_headers(item):
    global site_table, header_name_table, header_name_table_inverted, header_value_table, header_value_table_inverted, header_table, header_name_id, header_value_id, header_id
    site_id = item[0]
    site = item[1]
    url, code, headers = get_data(site)
    site_table[site_id] = [site, url, code]
    if code > 0:
        for header in headers:
            header_id += 1
            header_name = header[0]
            header_value = header[1]
            if header_name not in header_name_table.values():
                header_name_id += 1
                header_name_table[header_name_id] = header_name
                header_name_table_inverted[header_name] = header_name_id
                actual_header_name_id = header_name_id
            else:
                actual_header_name_id = header_name_table_inverted[header_name]
            if header_value not in header_value_table.values():
                header_value_id += 1
                header_value_table[header_value_id] = header_value
                header_value_table_inverted[header_value] = header_value_id
                actual_header_value_id = header_value_id
            else:
                actual_header_value_id = header_value_table_inverted[header_value]
            header_table[header_id] = [site_id, actual_header_name_id, actual_header_value_id]

def get_dictsites(filename):
    dictsites = {}
    with open(filename, 'rU') as f:
        for line in f:
            dictsites[int(line.strip().split(',')[0])] = line.strip().split(',')[1]
    return dictsites

def populate_mysql(site_table, header_name_table, header_value_table, header_table):
    print '\nPopulating MySQL tables'
    conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='headers')
    cursor = conn.cursor()
    print 'Table: site'
    for site_id in site_table.keys():
        site = site_table[site_id][0]
        url = site_table[site_id][1]
        code = site_table[site_id][2]
        cursor.execute('INSERT INTO `headers`.`site` (`site_id`, `site`, `url`, `code`) VALUES (%s, %s, %s, %s)', (site_id, site, url, code))
    print 'Table: header_value'
    for header_value_id in header_value_table.keys():
        value = header_value_table[header_value_id]
        cursor.execute('INSERT INTO `headers`.`header_value` (`header_value_id`, `value`) VALUES (%s, %s)', (header_value_id, value))
    print 'Table: header_name'
    for header_name_id in header_name_table.keys():
        name = header_name_table[header_name_id]
        cursor.execute('INSERT INTO `headers`.`header_name` (`header_name_id`, `name`) VALUES (%s, %s)', (header_name_id, name))
    print 'Table: header'
    for header_id in header_table.keys():
        site_id = header_table[header_id][0]
        header_name_id = header_table[header_id][1]
        header_value_id = header_table[header_id][2]
        cursor.execute('INSERT INTO `headers`.`header` (`header_id`, `site_id`, `header_name_id`, `header_value_id`) VALUES (%s, %s, %s, %s)', (header_id, site_id, header_name_id, header_value_id))
    conn.commit()
    cursor.close()
    conn.close()

def main():
    if len(sys.argv) != 3:
        print 'Invalid arguments!'
        sys.exit(1)
    filename = sys.argv[1]
    num_threads = int(sys.argv[2])
    dictsites = get_dictsites(filename)
    sites = len(dictsites)
    start = 0
    thread = 1
    while (start < sites):
        print 'Thread pool', thread, '(', start, '-', start+num_threads, ')'
        thread += 1
        threads = [gevent.spawn(work_headers, item) for item in dictsites.items()[start:start+num_threads]]
        gevent.joinall(threads)
        start += num_threads
    print '\nConnections summary', '\n', 'https:', chttps, '\n', 'http:', chttp, '\n', 'error:', cerror
    populate_mysql(site_table, header_name_table, header_value_table, header_table)

if __name__ == '__main__':
    main()