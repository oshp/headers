from lib.secureheaders.header import Header


class PublicKeyPins(Header):
    """ Publick-Key-Pins HTTP header  """

    name = 'public-key-pins'
    header_options = [
        '%pin-sha256%',
        '%max-age%',
        '%includeSubDomains%',
        '%report-uri%'
    ]
