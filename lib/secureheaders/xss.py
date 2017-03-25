import json

from lib.utils.queries import QTD_XSS_OTHER
from lib.utils.queries import COUNT_HEADER_BY_NAME
from lib.utils.queries import COUNT_HEADER_OPTION

class XSS(object):


    def __init__(self):
        self.name = 'x-xss-protection'
        self.options = {
            '0': COUNT_HEADER_OPTION.format(self.name, '0'),
            '0-mode-block': COUNT_HEADER_OPTION.format(self.name, '%0%mode=block%'),
            '1': COUNT_HEADER_OPTION.format(self.name, '1'),
            '1-mode-block': COUNT_HEADER_OPTION.format(self.name, '%1%mode=block%'),
            'report': COUNT_HEADER_OPTION.format(self.name, 'report'),
            'other': QTD_XSS_OTHER,
            'total': COUNT_HEADER_BY_NAME % self.name
        }
