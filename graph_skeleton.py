# Lazy Miner v.0.1.3
# @author: redjerdai

import numpy
import pandas

class GraphSkeleton:

    def __init__(self, configuration):

        self.nodes = Nodes()
        self.edges = Edges()
        self.configuration = configuration

    # TODO: add groups and clusters [16]
    # TODO: clarify all names [17]

    def feed_all(self, nodes_node_frame, edges_names, edges_weights,
                      nodes_back_colour_low=50, nodes_back_colour_up=200,
                      edges_boldness_low=0.5, edges_boldness_up=4):

        self.nodes.feed_nodes(node_frame=nodes_node_frame, name_column=self.configuration.nodes_names_column,
                              label_column=self.configuration.nodes_labels_column, weight_column=self.configuration.nodes_weights_column,
                              back_colour_column=self.configuration.nodes_back_colour_column,
                              back_colour_low=nodes_back_colour_low, back_colour_up=nodes_back_colour_up)
        self.edges.feed_edges(names=edges_names, weights=edges_weights,
                              boldness_low=edges_boldness_low, boldness_up=edges_boldness_up)


def str_vector(x):
    x = numpy.array(x, dtype=str)
    return x

def str_concat(x):
    return x[0] + x[1]

def str_vector_concat(a, b):

    if isinstance(a, numpy.ndarray):
        a_dimensionality = len(a.shape)
    else:
        a_dimensionality = 0
    if isinstance(b, numpy.ndarray):
        b_dimensionality = len(b.shape)
    else:
        b_dimensionality = 0

    if a_dimensionality == 1 and b_dimensionality == 0:
        b = numpy.array([b] * a.shape[0])
        b_dimensionality = 1
    if a_dimensionality == 0 and b_dimensionality == 1:
        a = numpy.array([a] * b.shape[0])
        a_dimensionality = 1

    if a_dimensionality == 1 and b_dimensionality == 1:
        c = {'a': a, 'b': b}
        c = pandas.DataFrame(data=c)
        d = c.apply(func=str_concat, axis=1)
        d = d.values
    else:
        if a_dimensionality == 0:
            d = numpy.full(shape=(b.shape[0], b.shape[1]), fill_value='', dtype=object)
            for i in range(b.shape[0]):
                for j in range(b.shape[1]):
                    d[i, j] = a + b[i, j]
        elif b_dimensionality == 0:
            d = numpy.full(shape=(a.shape[0], a.shape[1]), fill_value='', dtype=object)
            for i in range(a.shape[0]):
                for j in range(a.shape[1]):
                    d[i, j] = a[i, j] + b
        else:
            raise Exception('I do not know how to treat that (-_-) Seriously...')
    return d

def cut_hex(x):
    return hex(x)[2:]


def hex_vector(x):
    x = numpy.array(x, dtype=int)
    x = pandas.Series(x)
    x = x.apply(func=cut_hex)
    x = x.values
    return x


# TODO: Add check for consistency of inputs [16]
class Nodes:

    def __init__(self):

        # TODO: select better names (uniform and intuitive) [15]
        self.names = None
        self.labels = None
        self.weights = None
        self.back_colour_base = '#ffffff'
        self.back_colour_function = DefaultScaleFunction(conversion_function=hex_vector)
        self.back_colours = None

    def get_back_colour(self, value):

        scaled = self.back_colour_function.linear_scaling(value=value)
        result = str_vector_concat(self.back_colour_base, scaled)
        return result

    def feed_nodes(self, node_frame, name_column, label_column, weight_column, back_colour_column, back_colour_low, back_colour_up):

        self.names = node_frame[name_column].values
        self.labels = node_frame[label_column].values
        self.weights = node_frame[weight_column].values
        self.back_colour_function.feed(data=node_frame[back_colour_column].values, low_bound_target=back_colour_low, up_bound_target=back_colour_up)
        self.back_colours = self.get_back_colour(value=node_frame[back_colour_column].values)


class Edges:

    def __init__(self):

        self.names = None
        self.weights = None #numpy.zeros(shape=(dimensionality, dimensionality), dtype=int)
        self.boldness_base = ''
        self.boldness_function = DefaultScaleFunction(conversion_function=str_vector)
        self.boldness_values = None #numpy.full(shape=(dimensionality, dimensionality), fill_value=self.boldness_base, dtype='<U9')

    def get_boldness(self, value):

        scaled = self.boldness_function.linear_scaling(value=value)
        result = str_vector_concat(self.boldness_base, scaled)
        return result

    def feed_edges(self, names, weights, boldness_low, boldness_up):

        self.names = names
        self.weights = weights
        self.boldness_function.feed(data=weights, low_bound_target=boldness_low, up_bound_target=boldness_up)
        self.boldness_values = self.get_boldness(value=weights)


class DefaultScaleFunction:

    def __init__(self, conversion_function):

        self.low_bound_value = None
        self.low_bound_quantile = 0.1
        self.low_bound_target = None
        self.up_bound_value = None
        self.up_bound_quantile = 0.1
        self.up_bound_target = None
        self.scale_function = self.linear_scaling
        self.data = None
        self.conversion_function = conversion_function
        self.intercept = None
        self.coefficient = None

    def feed(self, data, low_bound_target, up_bound_target):

        self.data = data
        self.low_bound_value = numpy.quantile(a=self.data, q=self.low_bound_quantile)
        self.up_bound_value = numpy.quantile(a=self.data, q=(1 - self.up_bound_quantile))

        self.up_bound_target = up_bound_target
        self.low_bound_target = low_bound_target
        #print(self.up_bound_target)
        #print(self.low_bound_target)
        #print(self.up_bound_value)
        #print(self.low_bound_value)
        self.intercept = self.low_bound_target
        self.coefficient = (self.up_bound_target - self.low_bound_target) / (self.up_bound_value - self.low_bound_value)

        self.low_bound_target = low_bound_target
        self.up_bound_target = up_bound_target

    def linear_scaling(self, value):

        #print(self.intercept)
        #print(self.coefficient)
        #print(self.low_bound_value)
        #print(value)
        #print(value - self.low_bound_value)
        #print(self.coefficient * (value - self.low_bound_value))
        #print(self.intercept + self.coefficient * (value - self.low_bound_value))
        #print(self.conversion_function(self.intercept + self.coefficient * (value - self.low_bound_value)))

        scaled_value = numpy.where(value <= self.low_bound_value, self.conversion_function(self.low_bound_target),
                    numpy.where(value >= self.up_bound_value, self.conversion_function(self.up_bound_target),
                                self.conversion_function((self.intercept + self.coefficient * (value - self.low_bound_value)))))
        '''
        if value <= self.low_bound_value:
            scaled_value = self.conversion_function(value=self.low_bound_target)
        elif value >= self.up_bound_value:
            scaled_value = self.conversion_function(value=self.up_bound_target)
        else:
            scaled_value = self.conversion_function(value=(
                    self.intercept + self.coefficient * (value - self.low_bound_value)))
        '''

        return scaled_value

