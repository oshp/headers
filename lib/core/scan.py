import sys
import urllib2
from urlparse import urlparse
import socket
import httplib
import ssl

chttps = 0
chttp = 0
cerror = 0

class Scan:

    def __init__(self, settings):
        global chttps, chttp, cerror
        self.settings = settings

    def config_request(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def connection(self, url):
        ctx = self.config_request()

        req = urllib2.Request(url)
        req.add_header('User-Agent', self.settings['http']['user_agent'])
        req.add_header('Origin', self.settings['http']['origin'])
        try:
            response = urllib2.urlopen(
                req,
                timeout=self.settings['http']['timeout'],
                context=ctx)
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

    def get_data(self, site):
        global chttps, chttp, cerror
        url = 'https://' + site
        newurl, code, headers = self.connection(url) # Trying HTTPS
        if code < 0:
            url = 'http://' + site
            newurl, code, headers = self.connection(url) # Trying HTTP
            if code < 0:
                cerror += 1
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

    def get_summary(self):
        print ''
        print 'Connections summary'
        print 'https: {}'.format(chttps)
        print 'http: {}'.format(chttp)
        print 'error: {}'.format(cerror)
