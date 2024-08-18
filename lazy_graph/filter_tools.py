import pandas


class FilterTools:

    @staticmethod
    def by_edge(configuration, data, from_edge, to_edge):
        data = pandas.DataFrame(data)
        activity_name_lagged = configuration.activity_name + '_lagged'
        data = data[data[configuration.activity_name] == from_edge]
        data = data[data[activity_name_lagged] == to_edge]
        return data

    @staticmethod
    def by_way(configuration, data, from_edge, to_edge):
        ...

    @staticmethod
    def by_node(configuration, data, node_to_contain):
        data = pandas.DataFrame(data)
        data = data[data[configuration.activity_name] == node_to_contain]
        return data
