# coding: utf-8
import requests
import os

from urllib.parse import urlparse
from lib.utils.util import load_env_config
from requests.exceptions import (
    HTTPError, ConnectionError, Timeout
)


class Scan():

    chttp = 0
    chttps = 0
    cerror = 0

    def __init__(self):
        load_env_config()
        requests.packages.urllib3.disable_warnings()

    def connect(self, url, scheme='http'):
        headers = {
            'User-Agent': "OWASP SecureHeaders Project v4.0.0 (https://goo.gl/2SbYhw)",
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
                                    allow_redirects=True,
                                    verify=False)
            response_data['url'] = response.url
            response_data['status_code'] = response.status_code
            response_data['headers'] = {hname.lower(): hvalue.lower()
                for hname, hvalue in dict(response.headers).items()}
        except ConnectionError:
            print("[*] connection error for <{}>".format(url))
        except HTTPError:
            print("[*] error requesting <{}>...".format(url))
        except Timeout:
            print("[*] timeout expired for <{}>".format(url))
        else:
            return response_data

    def _gen_stats(self, code, url):
        if (400 <= code <= 500):
            self.cerror += 1
        elif code == 200:
            if urlparse(url).scheme == 'http':
                self.chttp += 1
            elif urlparse(url).scheme == 'https':
                self.chttps += 1

    def get_summary(self, sites):
        for site in sites:
            self._gen_stats(site['status_code'], site['url'])
        print('')
        print('Connections summary')
        print('https: {}'.format(self.chttps))
        print('http: {}'.format(self.chttp))
        print('error: {}'.format(self.cerror))
