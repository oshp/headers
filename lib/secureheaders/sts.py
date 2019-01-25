# coding: utf-8
from lib.secureheaders.header import Header


class StrictTransportSecurity(Header):

    name = 'strict-transport-security'
    header_options = [
        '%includeSubDomains%',
        '%max-age%'
    ]
