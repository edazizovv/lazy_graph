# Lazy Miner v.0.1.3
# @author: redjerdai

import pandas


class Reader:

    def __init__(self, configuration):

        self.configuration = configuration

    def read(self):

        data = None

        if self.configuration.extension == 'xlsx':

            data = pandas.read_excel(io=self.configuration.file)

        return data
