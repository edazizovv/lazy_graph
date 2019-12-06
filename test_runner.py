import os
import sys
import pandas

d = os.path.dirname(os.path.realpath(__file__))

if d not in sys.path:
    sys.path.append(d)

from lazy_miner import dfg_calculate_with_pandas

file = 'C:/Users/MainUser/Desktop/ШУЕ.xlsx'
case_id = 'case_id'
activity_name = 'activity_name'
time_stamp = 'time_stamp'
data = pandas.read_excel(io=file)

def mi_watchin():
    result_data, result_group = dfg_calculate_with_pandas(data=data, case_id=case_id, activity_name=activity_name, time_stamp=time_stamp)

