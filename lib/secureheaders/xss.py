# coding: utf-8
from lib.secureheaders.header import Header

from lib.utils.queries import QTD_XSS_OTHER


class XXssProtection(Header):
    """ X-XSS-Protection HTTP header  """

    name = 'x-xss-protection'
    header_options = [
        '%0%',
        '%0-mode-block%',
        '%1%',
        '%1-mode-block%',
        '%report%'
    ]
    extra_options = {
        'other': QTD_XSS_OTHER
    }
