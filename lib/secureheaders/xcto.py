from lib.secureheaders.header import Header

from lib.utils.queries import QTD_XCTO_OTHER


class XContentTypeOptions(Header):
    """ X-Content-Type-Options HTTP header  """

    name = 'x-content-type-options'
    header_options = [
        '%nosniff%'
    ]
    extra_options = {
        'other': QTD_XCTO_OTHER
    }
