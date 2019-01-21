import requests
import os

from urllib.parse import urlparse
import socket

from lib.utils.util import load_env_config

from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout

from lib.utils.config import HTTP_SCHEME
from lib.utils.config import HTTPS_SCHEME
from lib.utils.config import NO_SCHEME
from lib.utils.config import HTTP_STATUS_CODE
from lib.utils.config import SITE

from collections import deque

class Scan():

    def __init__(self):
        load_env_config()
        self._fallback = deque([
            'www', 'm', 'ftp', 
            'webmail', 'blog', 'wiki'])
    
    def __generate_uri(self, url):
        if len(self._fallback) > 0:
            subdomain = self._fallback.pop()
            return "{}.{}".format(subdomain, url)

    def connection(self, url, scheme='http'):
        headers = {
            'User-Agent': "OWASP SecureHeaders Project v3.3.x (https://goo.gl/2SbYhw)",
            'Origin': "{}".format(os.getenv('ORIGIN'))
        }
        response_data = {
            "url": "",
            "status_code": "",
            "headers": {}
        }
        uri = "{}://{}".format(scheme, url)
        try:
            response = requests.get(uri, 
                                    headers=headers, 
                                    timeout=3,
                                    allow_redirects=True)
            response_data['url'] = response.url
            response_data['status_code'] = response.status_code
            response_data['headers'] = {hname.lower(): hvalue.lower() 
                for hname,hvalue in dict(response.headers).items()}
        except ConnectionError:
            print("[*] connection error for <{}>".format(url))
            print("[*] trying fallback...")
            self.connection(self.__generate_uri(url))
        except HTTPError:
            print("[*] error requesting <{}>...".format(url))
            print("[*] trying fallback...")
            self.connection(self.__generate_uri(url))
        except Timeout:
            print("[*] timeout expired for <{}>".format(url))
            print("[*] trying fallback...")
            self.connection(self.__generate_uri(url))
        else:
            return response_data

    def gen_stats(self, code, url, scheme):
        if (code == 200 or code < 0) and urlparse(url).scheme == scheme:
            yield 1
        else:
            yield 0

    def get_summary(self, site_table):
        chttp = 0
        chttps = 0
        cerror = 0
        for site in site_table:
            chttps += next(self.gen_stats(site[HTTP_STATUS_CODE], site[SITE], HTTPS_SCHEME))
            chttp += next(self.gen_stats(site[HTTP_STATUS_CODE], site[SITE], HTTP_SCHEME))
            cerror += next(self.gen_stats(site[HTTP_STATUS_CODE], site[SITE], NO_SCHEME))
        print('')
        print('Connections summary')
        print('https: {}'.format(chttps))
        print('http: {}'.format(chttp))
        print('error: {}'.format(cerror))
