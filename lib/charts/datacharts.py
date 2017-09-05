from lib.database.db import DB
from lib.cache.datacache import Datacache

from lib.secureheaders.xss import XSS
from lib.secureheaders.xfo import XFO
from lib.secureheaders.xcto import XCTO
from lib.secureheaders.sts import STS
from lib.secureheaders.pkp import PKP
from lib.secureheaders.csp import CSP
from lib.secureheaders.sites import Sites

class Datacharts(object):


    def __init__(self, settings):
        self.db = DB(settings)
        self.cache = Datacache(settings)

    def make_query(self, data):
        datachart = {}
        for key, query in data.iteritems():
            results = self.db.query(query)
            for data_value in results:
                datachart[key] = data_value[0]
        return datachart

    def get_datachart(self, key, data):
        datachart = {}
        if self.cache.check_cache(key):
            datachart = self.cache.get_data_cache(key)
        else:
            datachart = self.make_query(data)
            self.cache.add_in_cache(key, datachart)
        return datachart

    def get_xss_datachart(self):
        xss = XSS()
        return self.get_datachart(xss.name, xss.options)

    def get_pkp_datachart(self):
        pkp = PKP()
        return self.get_datachart(pkp.name, pkp.options)

    def get_xfo_datachart(self):
        xfo = XFO()
        return self.get_datachart(xfo.name, xfo.options)

    def get_xcto_datachart(self):
        xcto = XCTO()
        return self.get_datachart(xcto.name, xcto.options)

    def get_sts_datachart(self):
        sts = STS()
        return self.get_datachart(sts.name, sts.options)

    def get_csp_datachart(self):
        csp = CSP()
        return self.get_datachart(csp.name, csp.options)

    def get_total_sites(self):
        return self.get_datachart(sites.sites, sites.options)
