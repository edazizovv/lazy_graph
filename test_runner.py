# Lazy Miner v.0.1.6
# @author: redjerdai

import os
import sys
import numpy
import pandas

d = os.path.dirname(os.path.realpath(__file__))

if d not in sys.path:
    sys.path.append(d)

from lazy_miner import dfg_calculate_with_pandas
from configuration import Configuration
from readers import Reader
from graph_skeleton import GraphSkeleton
from filter_tools import FilterTools
from visualisation_tools import VisualisationTools



configuration = Configuration()
#configuration.file = 'C:/Users/MainUser/Desktop/ШУЕ.xlsx'
configuration.file = 'C:/Users/MainUser/Desktop/gex.xlsx'
configuration.case_id = 'Title'
configuration.activity_name = 'Position'
configuration.time_stamp = 'DateTime'
configuration.nodes_names_column = 'Position'


reader = Reader(configuration=configuration)
data = reader.read()

# graph

graph = GraphSkeleton(configuration=configuration, nodes_back_colour_base='#800080')

#result_data, result_group, edges, router, weights = dfg_calculate_with_pandas(configuration=configuration, data=data)
data_new, nodes_frame, timie, edges, weights, activities = dfg_calculate_with_pandas(configuration=configuration, data=data)
edges_colour_matrix = numpy.full(shape=(weights.shape[0], weights.shape[1]), fill_value='black', dtype='<U5')

graph.feed_all(nodes_node_frame=nodes_frame, nodes_names=activities, edges_names=edges, edges_weights=weights)
graph.draw()

# distributions

# (I want all those who went from 'sleep' to 'farm'

my_filtered = FilterTools.by_edge(configuration=configuration, data=data_new, from_edge='HeadlineList-4', to_edge='HeadlineList-5')
#VisualisationTools.simple_hist(array=my_filtered[configuration.duration])
VisualisationTools.estimate_hist(configuration=configuration, array=my_filtered[configuration.duration])
