import urllib2
from urlparse import urlparse
import socket
import httplib

from lib.utils.config import HTTP_SCHEME
from lib.utils.config import HTTPS_SCHEME
from lib.utils.config import NO_SCHEME
from lib.utils.config import HTTP_STATUS_CODE
from lib.utils.config import SITE

class Scan(object):


    def __init__(self, settings):
        self.settings = settings

    def connection(self, url, scheme=HTTPS_SCHEME):
        site = scheme + '://' + url
        req = urllib2.Request(site)
        req.add_header('User-Agent', self.settings['http']['user_agent'])
        req.add_header('Origin', self.settings['http']['origin'])
        try:
            response = urllib2.urlopen(req, timeout=3)
        except socket.error as error:
            return str(error), -1, ''
        except urllib2.URLError as error:
            return str(error.reason), -2, ''
        except httplib.HTTPException as error:
            return str(error), -3, ''
        else:
            return response.geturl(), response.getcode(), response.info().items()

    def get_data(self, site):
        newurl, code, headers = self.connection(site)
        if code < 0:
            newurl, code, headers = self.connection(site, HTTP_SCHEME)
        return newurl, code, headers

    def test_scheme(self, code, url, scheme):
        if (code == 200 or code < 0) and urlparse(url).scheme == scheme:
            yield 1
        else:
            yield 0

    def gen_stats(self, code, url, scheme):
        return self.test_scheme(code, url, scheme)

    def get_summary(self, site_table):
        chttp = 0
        chttps = 0
        cerror = 0
        for site in site_table:
            chttps += self.gen_stats(site[HTTP_STATUS_CODE], site[SITE], HTTPS_SCHEME).next()
            chttp += self.gen_stats(site[HTTP_STATUS_CODE], site[SITE], HTTP_SCHEME).next()
            cerror += self.gen_stats(site[HTTP_STATUS_CODE], site[SITE], NO_SCHEME).next()
        print('')
        print('Connections summary')
        print('https: {}').format(chttps)
        print('http: {}').format(chttp)
        print('error: {}').format(cerror)
