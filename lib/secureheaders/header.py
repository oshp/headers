from lib.charts.datacharts import Datacharts

from lib.utils.queries import COUNT_HEADER_BY_NAME
from lib.utils.queries import COUNT_HEADER_OPTION


class Header():

    name = "Generic HTTP Header"
    header_options = []
    extra_options = {}
    options = {}

    def __init__(self):
        self.datachart = Datacharts()

    def __has_extra_options(self):
        if len(self.extra_options) > 0:
            self.options.update(self.extra_options)

    def __format_option(self, option_name):
        local_name = option_name.split('%')
        if len(local_name) == 3:
            return local_name[1]
        else:
            return option_name

    def __configure_properties(self):
        [self.options.update({self.__format_option(header_option):
                              COUNT_HEADER_OPTION.format(self.name,
                                                         header_option)})
         for header_option in self.header_options]
        self.options.update({'total': COUNT_HEADER_BY_NAME.format(header_name=self.name)})
        self.__has_extra_options()

    def make_query(self):
        self.__configure_properties()
        return self.datachart.make_query(self.options)

    def get_datachart(self):
        self.__configure_properties()
        return self.datachart.get_datachart(self.name, self.options)
