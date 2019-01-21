from lib.secureheaders.header import Header


class ContentSecurityPolicy(Header):
    """ Content-Security-Policy HTTP header  """

    name = 'content-security-policy'
    header_options = [
        '%report-uri%',
        '%default-src%',
        '%script-nonce%',
        '%script-nonce%',
        '%upgrade-insecure-requests%',
        '%media-src%',
        '%report-to%',
        '%reflected-xss%',
        '%style-src%',
        '%frame-src%',
        '%block-all-mixed-content%',
        '%child-src%',
        '%form-action%',
        '%base-uri%',
        '%img-src%',
        '%frame-ancestors%',
        '%manifest-src%',
        '%referrer%',
        '%sandbox%',
        '%plugin-types%',
        '%object-src%',
        '%connect-src%',
        '%font-src%',
        '%script-src%'
    ]
