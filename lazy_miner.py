# Lazy Miner v.0.1.0
# @author: redjerdai

import numpy
import pandas
import datetime

# TODO: refactor according to PEP 8


def initial_check(data, case_id, activity_name, time_stamp):

    data_checked = any([isinstance(data, numpy.ndarray), isinstance(data, pandas.DataFrame)])
    fields_checked = all([isinstance(case_id, str), isinstance(activity_name, str), isinstance(time_stamp, str)])
    # TODO: check that 'time_stamp' field is in ISO format
    if not all([data_checked, fields_checked]):
        raise ValueError("Invalid data types\nReminder: 'data' should be either numpy.ndarray or pandas.DataFrame; "
                         "'case_id', 'activity_name', 'time_stamp' should all be strings")
    return None


def dfg_calculate_with_numpy(data, case_id, activity_name, time_stamp):

    # TODO: implement faster algorithm with numpy

    # Check input types
    initial_check(data=data, case_id=case_id, activity_name=activity_name, time_stamp=time_stamp)

    # Ensure that 'data' is numpy.ndarray
    if isinstance(data, pandas.DataFrame):
        columns_list = data.columns.values.tolist()
        case_id = columns_list.index(case_id)
        activity_name = columns_list.index(activity_name)
        time_stamp = columns_list.index(time_stamp)
        data = data.values

    # Sort time stamp field
    data = data[data[:, time_stamp].argsort()]

    # Form
    ...


def dfg_calculate_with_pandas(data, case_id, activity_name, time_stamp, agg_func='mean'):

    # Check input types
    initial_check(data=data, case_id=case_id, activity_name=activity_name, time_stamp=time_stamp)

    # Ensure that 'data' is pandas.DataFrame
    if isinstance(data, numpy.ndarray):
        data_dict = {'case_id': data[:, case_id],
                     'activity_name': data[:, activity_name],
                     'time_stamp': data[:, time_stamp]}
        case_id, activity_name, time_stamp = 'case_id', 'activity_name', 'time_stamp'
        data = pandas.DataFrame(data_dict)

    # Sort time stamp field
    data = data.sort_values(by=[time_stamp], axis='index')

    # TODO: rename these postfixes
    # Tectonic shift
    case_id_lagged = case_id + '_lagged'
    activity_name_lagged = activity_name + '_lagged'
    time_stamp_lagged = time_stamp + '_lagged'
    data[[case_id_lagged, activity_name_lagged, time_stamp_lagged]] = data[[case_id, activity_name, time_stamp]].shift(periods=-1, axis=0)
    data = data.dropna()
    data = data[data[case_id] == data[case_id_lagged]]
    # TODO: add option to select time units
    data[time_stamp], data[time_stamp_lagged] = data[time_stamp].astype(dtype=numpy.datetime64), data[time_stamp_lagged].astype(dtype=numpy.datetime64)
    data['case_duration'] = data[time_stamp_lagged] - data[time_stamp]
    data['case_duration'] = data['case_duration'].astype(dtype=numpy.timedelta64)
    group = data.groupby([case_id, case_id_lagged]).agg(agg_func)

    return data, group
