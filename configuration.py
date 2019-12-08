# Lazy Miner v.0.1.3
# @author: redjerdai


class Configuration:

    def __init__(self):

        self.file = 'C:/Users/MainUser/Desktop/ШУЕ.xlsx'
        self.extension = 'xlsx'

        self.case_id = 'case_id'
        self.activity_name = 'activity_name'
        self.time_stamp = 'time_stamp'
        self.duration = 'case_duration'

        self.agg_func = 'mean'

        self.nodes_border_colour_enabled = False
        self.nodes_border_colour_low = None
        self.nodes_border_colour_up = None

        self.nodes_back_colour_enabled = True
        self.nodes_back_colour_low = 200
        self.nodes_back_colour_up = 50

        self.nodes_border_boldness_enabled = False
        self.nodes_border_boldness_low = None
        self.nodes_border_boldness_up = None

        self.edges_boldness_enabled = True
        self.edges_boldness_low = 0.5
        self.edges_boldness_up = 4

        self.edges_colour_enabled = False
        self.edges_colour_low = None
        self.edges_colour_up = None

