from lib.utils.queries import COUNT_HEADER_BY_NAME
from lib.utils.queries import COUNT_HEADER_OPTION

class CSP(object):

    def __init__(self):
        self.name = 'content-security-policy'
        self.options = {
            'report-uri': COUNT_HEADER_OPTION.format(self.name, 'report-uri'),
            'default-src': COUNT_HEADER_OPTION.format(self.name, 'default-src'),
            'script-nonce': COUNT_HEADER_OPTION.format(self.name, 'script-nonce'),
            'upgrade-insecure-requests': COUNT_HEADER_OPTION.format(self.name, 'upgrade-insecure-requests'),
            'media-src': COUNT_HEADER_OPTION.format(self.name, 'media-src'),
            'report-to': COUNT_HEADER_OPTION.format(self.name, 'report-to'),
            'reflected-xss': COUNT_HEADER_OPTION.format(self.name, 'reflected-xss'),
            'style-src': COUNT_HEADER_OPTION.format(self.name, 'style-src'),
            'frame-src': COUNT_HEADER_OPTION.format(self.name, 'frame-src'),
            'block-all-mixed-content': COUNT_HEADER_OPTION.format(self.name, 'block-all-mixed-content'),
            'child-src': COUNT_HEADER_OPTION.format(self.name, 'child-src'),
            'form-action': COUNT_HEADER_OPTION.format(self.name, 'form-action'),
            'base-uri': COUNT_HEADER_OPTION.format(self.name, 'base-uri'),
            'img-src': COUNT_HEADER_OPTION.format(self.name, 'img-src'),
            'frame-ancestors': COUNT_HEADER_OPTION.format(self.name, 'frame-ancestors'),
            'manifest-src': COUNT_HEADER_OPTION.format(self.name, 'manifest-src'),
            'referrer': COUNT_HEADER_OPTION.format(self.name, 'referrer'),
            'sandbox': COUNT_HEADER_OPTION.format(self.name, 'sandbox'),
            'plugin-types': COUNT_HEADER_OPTION.format(self.name, 'plugin-types'),
            'object-src': COUNT_HEADER_OPTION.format(self.name, 'object-src'),
            'connect-src': COUNT_HEADER_OPTION.format(self.name, 'connect-src'),
            'font-src': COUNT_HEADER_OPTION.format(self.name, 'font-src'),
            'script-src': COUNT_HEADER_OPTION.format(self.name, 'script-src'),
            'total': COUNT_HEADER_BY_NAME % self.name
        }
