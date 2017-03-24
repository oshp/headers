from lib.utils.queries import COUNT_HEADER_BY_NAME
from lib.utils.queries import COUNT_HEADER_OPTION

class PKP(object):

    def __init__(self):
        self.name = 'public-key-pins'
        self.options = {
                'pin-sha256': COUNT_HEADER_OPTION.format(self.name, 'pin-sha256'),
                'max-age': COUNT_HEADER_OPTION.format(self.name, 'max-age'),
                'includeSubDomains': COUNT_HEADER_OPTION.format(self.name, 'includeSubDomains'),
                'report-uri': COUNT_HEADER_OPTION.format(self.name, 'report-uri'),
                'total': COUNT_HEADER_BY_NAME % self.name
            }
