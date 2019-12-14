# Lazy Miner v.0.1.6
# @author: redjerdai

import numpy
from matplotlib import pyplot


class VisualisationTools:

    @staticmethod
    def simple_hist(array, n_bins=100):

        y, binEdges = numpy.histogram(array, bins=100, density=True)
        bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])

        pyplot.plot(bincenters, y, 'b-')
        #pyplot.hist(x=array, bins=n_bins, density=True)
        pyplot.savefig('hist.png')

        return None

    @staticmethod
    def estimate_hist(configuration, array, n_bins=100, sample_size=(10000,), estimator_params=None):

        generated = configuration.hist_estimator(data=array, sample_size=sample_size, estimator_params=estimator_params)

        y, binEdges = numpy.histogram(array, bins=100, density=True)
        bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])

        fig, ax = pyplot.subplots()
        ax.plot(bincenters, y, 'b-')
        ax.hist(x=generated, bins=n_bins, density=True)
        fig.savefig('hist.png')

        return None
