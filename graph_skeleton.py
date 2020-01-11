# Lazy Miner v.0.1.6
# @author: redjerdai
# TODO: Add graphviz configuration options [10]
import numpy
import pandas

import os
os.environ["PATH"] += os.pathsep + 'E:\\RAMP-EXTERNAL\\IP-02\\OSTRTA\\graphviz-2.38\\release\\bin'
from graphviz import Digraph

# TODO: make nodes and edges class entities [11]
# TODO: remove router; it should be gained automatically from weights / we should compare with zeros [13]
# TODO: check input data [14]


class GraphSkeleton:

    def __init__(self, configuration, nodes_back_colour_base='#ffffff'):

        self.nodes = Nodes(back_colour_base=nodes_back_colour_base)
        self.edges = Edges()
        self.configuration = configuration

    # TODO: add groups and clusters [16]
    # TODO: clarify all names [17]

    def feed_all(self, nodes_node_frame, nodes_names, edges_names, edges_weights,
                      nodes_back_colour_low=50, nodes_back_colour_up=200,
                      edges_boldness_low=0.5, edges_boldness_up=4):

        self.nodes.feed_nodes(activity_name=self.configuration.activity_name,
                              node_frame=nodes_node_frame, nodes_names=nodes_names,
                              weight_column=self.configuration.nodes_weights_column,
                              back_colour_column=self.configuration.nodes_back_colour_column,
                              back_colour_low=nodes_back_colour_low, back_colour_up=nodes_back_colour_up)
        self.edges.feed_edges(names=edges_names, weights=edges_weights,
                              boldness_low=edges_boldness_low, boldness_up=edges_boldness_up)

    def draw(self):

        # border_colouring, back_colouring, clustering, shaping, bordering,
        graph = Digraph(comment='pydge')

        # adding nodes
        for k in range(self.nodes.n()):
            # TODO: add such additional parameters as: border line style [12]
            graph.node(name=self.nodes.names[k], label=self.nodes.labels[k],
                       color='#000000',
                       fillcolor=self.nodes.back_colours[k],
                       penwidth='1',
                       style='filled')

        # adding edges
        #print(self.edges.names)
        #print(self.edges.router)
        #print(self.edges.n())
        '''
        for k in range(self.edges.m()):
            _from = self.nodes.names.tolist().index(self.edges.names[k, 0])
            _to = self.nodes.names.tolist().index(self.edges.names[k, 1])
        '''

        for i in range(self.edges.n()):
            for j in range(self.edges.n()):
                if self.edges.router[i, j]:
                    #print(self.nodes.names[i])
                    #print(self.nodes.names[j])
                    #print(self.edges.boldness_values[i])
                    graph.edge(tail_name=self.nodes.names[i], head_name=self.nodes.names[j],
                               label=str(self.edges.weights[i, j]), penwidth=str(self.edges.boldness_values[i, j]),
                               style='solid')

        graph.view()


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

    def __init__(self, back_colour_base):

        # TODO: select better names (uniform and intuitive) [15]
        self.names = None
        self.labels = None
        self.weights = None
        self.back_colour_base = back_colour_base
        self.back_colour_function = DefaultScaleFunction(conversion_function=hex_vector)
        self.back_colours = None

    def get_back_colour(self, value):

        scaled = self.back_colour_function.linear_scaling(value=value)
        result = str_vector_concat(self.back_colour_base, scaled)
        return result

    def feed_nodes(self, activity_name, node_frame, nodes_names, weight_column, back_colour_column, back_colour_low, back_colour_up):

        #self.names = node_frame[name_column].values
        self.names = nodes_names
        self.labels = nodes_names#node_frame[label_column].values
        self.weights = node_frame[weight_column].values
        self.back_colour_function.feed(data=node_frame[back_colour_column].values, low_bound_target=back_colour_low, up_bound_target=back_colour_up)
        #print(node_frame)
        a = node_frame.sort_values(by=activity_name)
        #a = numpy.sort()
        #print(a)
        self.back_colours = self.get_back_colour(value=a[back_colour_column].values)

    def n(self):

        return self.names.shape[0]


class Edges:

    def __init__(self):

        # TODO: names is a misleading name for this field, it should be changed [18]
        self.names = None
        self.router = None
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
        self.router = numpy.array(self.weights, dtype=bool)

    def m(self):
        return self.names.shape[0]

    def n(self):
        return self.router.shape[0]


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

