# coding: utf-8
from collections import UserDict


class Site(UserDict):

    def __init__(self, data):
        self.data = data
        self.data.update({'headers':{}})