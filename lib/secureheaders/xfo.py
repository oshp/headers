from lib.utils.queries import QTD_XFO_OTHER
from lib.utils.queries import COUNT_HEADER_BY_NAME
from lib.utils.queries import COUNT_HEADER_OPTION
from lib.utils.queries import COUNT_HEADER_OPTION_SIMPLE

class XFO(object):


    def __init__(self):
        self.name = 'x-frame-options'
        self.options = {
            'deny': COUNT_HEADER_OPTION_SIMPLE.format(self.name, 'deny'),
            'sameorigin': COUNT_HEADER_OPTION_SIMPLE.format(self.name, 'sameorigin'),
            'allow-from': COUNT_HEADER_OPTION.format(self.name, '%allow-from%'),
            'other': QTD_XFO_OTHER,
            'total': COUNT_HEADER_BY_NAME % self.name
        }
