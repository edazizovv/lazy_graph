# Lazy Miner v.0.1.1
# @author: redjerdai

import os
import sys
import numpy
import pandas

d = os.path.dirname(os.path.realpath(__file__))

if d not in sys.path:
    sys.path.append(d)

from lazy_miner import dfg_calculate_with_pandas
from visualiser import visualise

file = 'C:/Users/MainUser/Desktop/ШУЕ.xlsx'
case_id = 'case_id'
activity_name = 'activity_name'
time_stamp = 'time_stamp'
data = pandas.read_excel(io=file)

#def mi_watchin():
result_data, result_group, edges, router, weights = dfg_calculate_with_pandas(data=data, case_id=case_id, activity_name=activity_name, time_stamp=time_stamp)

# some temporal substitutions
nodes_names, nodes_counts = numpy.unique(ar=data[activity_name].values, return_counts=True)
subs = []
for k in range(nodes_names.shape[0]):
    add = pandas.DataFrame(data={'name': [str(nodes_names[k])], 'label': [str(nodes_counts[k])],
                                 'border_colouring': ['black'], 'back_colouring': ['white'], 'boldness': ['1']})
    subs.append(add)
del add
nodes_options = pandas.concat(objs=subs, axis=0, ignore_index=True)
edges_styles = numpy.array([['solid'] * router.shape[0]] * router.shape[0])
edges_boldness = numpy.ones(shape=(router.shape[0], router.shape[0]), dtype=str)


# here goes visualisation

visualise(nodes_options=nodes_options, router=router, weights=weights, edges_styles=edges_styles,
          edges_boldness=edges_boldness)
