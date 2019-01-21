from lib.secureheaders.header import Header


class XPermittedCrossDomainPolicies(Header):
    """ XPermittedCrossDomainPolicies HTTP header  """

    name = 'x-permitted-cross-domain-policies'
    header_options = [
        '%none%',
        '%master-only%',
        '%by-content-type%',
        '%by-ftp-filename%',
        '%all%'
    ]
