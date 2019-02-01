# coding: utf-8
from lib.secureheaders.header import Header

from lib.utils.queries import QTD_XFO_OTHER


class XFrameOptions(Header):
    """ X-Frame-Options HTTP header  """

    name = 'x-frame-options'
    header_options = [
        'deny',
        'sameorigin',
        '%allow-from%'
    ]
    extra_options = {
        'other': QTD_XFO_OTHER
    }
