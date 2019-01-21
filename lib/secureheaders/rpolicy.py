from lib.secureheaders.header import Header


class ReferrerPolicy(Header):
    """ Referrer-Policy HTTP header  """

    name = 'referrer-policy'
    header_options = [
        '%no-referrer%',
        '%no-referrer-when-downgrade%',
        '%origin%',
        '%origin-when-cross-origin%',
        '%same-origin%',
        '%ostrict-origin%',
        '%strict-origin-when-cross-origin%',
        '%unsafe-url%'
    ]
