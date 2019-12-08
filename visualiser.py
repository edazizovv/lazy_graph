# Lazy Miner v.0.1.2
# @author: redjerdai

# TODO: Add graphviz configuration options [10]
import os
os.environ["PATH"] += os.pathsep + 'C:\\Sygm\\RAMP\\IP-02\\OSTRTA\\graphviz-2.38\\release\\bin'
from graphviz import Digraph


# TODO: make nodes and edges class entities [11]
# TODO: remove router; it should be gained automatically from weights / we should compare with zeros [13]
# TODO: check input data [14]
def visualise(nodes_options, router, weights, edges_styles, edges_boldness):
    # border_colouring, back_colouring, clustering, shaping, bordering,
    graph = Digraph(comment='pydge')

    # adding nodes
    for k in range(nodes_options.shape[0]):
        # TODO: add such additional parameters as: border line style [12]
        graph.node(name=nodes_options.loc[k, 'name'], label=nodes_options.loc[k, 'label'],
                   color=nodes_options.loc[k, 'border_colouring'],
                   fillcolor=nodes_options.loc[k, 'back_colouring'],
                   penwidth=nodes_options.loc[k, 'boldness'],
                   style="filled")

    # adding edges
    for i in range(router.shape[0]):
        for j in range(router.shape[1]):
            if router[i, j]:
                graph.edge(tail_name=nodes_options.loc[i, 'name'], head_name=nodes_options.loc[j, 'name'],
                           label=str(weights[i, j]), penwidth=edges_boldness[i, j],
                           style=edges_styles[i, j])

    graph.view()
    #graph.render('C:/Users/MainUser/Desktop/graph', view=True)

