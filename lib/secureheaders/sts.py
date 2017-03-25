from lib.utils.queries import COUNT_HEADER_OPTION
from lib.utils.queries import COUNT_HEADER_BY_NAME

class STS(object):


    def __init__(self):
        self.name = 'strict-transport-security'
        self.options = {
            'includeSubDomains': COUNT_HEADER_OPTION.format(self.name, 'includeSubDomains'),
            'max-age': COUNT_HEADER_OPTION.format(self.name, 'max-age'),
            'total': COUNT_HEADER_BY_NAME % self.name
        }
