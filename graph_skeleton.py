# Lazy Miner v.0.1.3
# @author: redjerdai

import numpy


class GraphSkeleton:

    def __init__(self):

        self.nodes = Nodes()
        self.edges = Edges()

    # TODO: add groups and clusters [16]

    def feed_all(self, data, nodes_border_colour_low, nodes_border_colour_up, nodes_back_colour_low, nodes_back_colour_up, nodes_border_boldness_low, nodes_border_boldness_up, edges_boldness_low, edges_boldness_up, edges_colour_low, edges_colour_up):

        self.nodes.feed_scale_functions(data=data, border_colour_low=nodes_border_colour_low, border_colour_up=nodes_border_colour_up,
                                        back_colour_low=nodes_back_colour_low, back_colour_up=nodes_back_colour_up,
                                        border_boldness_low=nodes_border_boldness_low, border_boldness_up=nodes_border_boldness_up)

        self.edges.feed_scale_functions(data=data, boldness_low=edges_boldness_low, boldness_up=edges_boldness_up, colour_low=edges_colour_low, colour_up=edges_colour_up)

    def construct_all(self, nodes_node_frame, nodes_name_column, nodes_label_column, nodes_weight_column, nodes_border_colour_column, nodes_back_colour_column, nodes_border_boldness_column, edges_names, edges_weights, edges_boldness_valued_matrix, edges_colour_valued_matrix):

        self.nodes.feed_nodes(node_frame=nodes_node_frame, name_column=nodes_name_column, label_column=nodes_label_column, weight_column=nodes_weight_column, border_colour_column=nodes_border_colour_column, back_colour_column=nodes_back_colour_column, border_boldness_column=nodes_border_boldness_column)
        self.edges.feed_edges(names=edges_names, weights=edges_weights, boldness_valued_matrix=edges_boldness_valued_matrix, colour_valued_matrix=edges_colour_valued_matrix)


def as_is(x):
    return x


# TODO: Add check for consistency of inputs [16]
class Nodes:

    def __init__(self):

        # TODO: select better names (uniform and intuitive) [15]
        self.names = None
        self.labels = None
        self.weights = None
        self.border_colour_base = '#000000'
        self.border_colour_function = DefaultScaleFunction(conversion_function=hex)
        self.border_colours = None
        self.back_colour_base = '#ffffff'
        self.back_colour_function = DefaultScaleFunction(conversion_function=hex)
        self.back_colours = None
        self.border_boldness_base = ''
        self.border_boldness_function = DefaultScaleFunction(conversion_function=as_is)
        self.border_boldness_values = None

    def feed_scale_functions(self, data, border_colour_low, border_colour_up, back_colour_low, back_colour_up, border_boldness_low, border_boldness_up):

        self.border_colour_function.feed(data=data, low_bound_target=border_colour_low, up_bound_target=border_colour_up)
        self.back_colour_function.feed(data=data, low_bound_target=back_colour_low, up_bound_target=back_colour_up)
        self.border_boldness_function.feed(data=data, low_bound_target=border_boldness_low, up_bound_target=border_boldness_up)

    def get_border_colour(self, value):

        scaled = self.border_colour_function.linear_scaling(value=value)
        result = self.border_colour_base + scaled
        return result

    def get_back_colour(self, value):

        scaled = self.back_colour_function.linear_scaling(value=value)
        result = self.back_colour_base + scaled
        return result

    def get_border_boldness(self, value):

        scaled = self.border_boldness_function.linear_scaling(value=value)
        result = self.border_boldness_base + scaled
        return result

    def feed_nodes(self, node_frame, name_column, label_column, weight_column, border_colour_column, back_colour_column, border_boldness_column):

        self.names = node_frame[name_column].values
        self.labels = node_frame[label_column].values
        self.weights = node_frame[weight_column].values
        self.border_colours = self.get_border_colour(value=node_frame[border_colour_column].values)
        self.back_colours = self.get_back_colour(value=node_frame[back_colour_column].values)
        self.border_boldness_values = self.get_border_boldness(value=node_frame[border_boldness_column].values)


class Edges:

    def __init__(self):

        self.names = None
        self.weights = None #numpy.zeros(shape=(dimensionality, dimensionality), dtype=int)
        self.boldness_base = ''
        self.boldness_function = ...
        self.boldness_values = None #numpy.full(shape=(dimensionality, dimensionality), fill_value=self.boldness_base, dtype='<U9')
        self.colour_base = '#000000'
        self.colour_function = ...
        self.colour_values = None #numpy.full(shape=(dimensionality, dimensionality), fill_value=self.colour_base, dtype='<U9')

    def feed_scale_functions(self, data, boldness_low, boldness_up, colour_low, colour_up):

        self.boldness_function.feed(data=data, low_bound_target=boldness_low, up_bound_target=boldness_up)
        self.colour_function.feed(data=data, low_bound_target=colour_low, up_bound_target=colour_up)

    def get_boldness(self, value):

        scaled = self.boldness_function.linear_scaling(value=value)
        result = self.boldness_base + scaled
        return result

    def get_colour(self, value):

        scaled = self.colour_function.linear_scaling(value=value)
        result = self.colour_base + scaled
        return result

    def feed_edges(self, names, weights, boldness_valued_matrix, colour_valued_matrix):

        self.names = names
        self.weights = weights
        self.boldness_values = self.get_boldness(value=boldness_valued_matrix)
        self.colour_values = self.get_colour(value=colour_valued_matrix)


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
        self.intercept = self.low_bound_target
        self.coefficient = (self.up_bound_target - self.low_bound_target) / (self.up_bound_value - self.low_bound_value)

        self.low_bound_target = low_bound_target
        self.up_bound_target = up_bound_target

    def linear_scaling(self, value):

        if value <= self.low_bound_value:
            scaled_value = self.conversion_function(value=self.low_bound_target)
        elif value >= self.up_bound_value:
            scaled_value = self.conversion_function(value=self.up_bound_target)
        else:
            scaled_value = self.conversion_function(value=(
                    self.intercept + self.coefficient * (value - self.low_bound_value)))
        return scaled_value

