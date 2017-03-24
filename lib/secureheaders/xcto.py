from lib.utils.queries import QTD_XCTO_OTHER
from lib.utils.queries import COUNT_HEADER_BY_NAME
from lib.utils.queries import COUNT_HEADER_OPTION

class XCTO(object):

    def __init__(self):
        self.name = 'x-content-type-options'
        self.options = {
            'nosniff': COUNT_HEADER_OPTION.format(self.name, 'nosniff'),
            'other': QTD_XCTO_OTHER,
            'total': (COUNT_HEADER_BY_NAME % self.name)
        }

    def total(self):
        return COUNT_HEADER_BY_NAME % self.name
