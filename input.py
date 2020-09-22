import datetime
import os
import pandas as pd


def input_data(file_path):
    data = dict()
    for file in os.listdir(file_path):
        data[file] = \
            pd.read_csv(
                'data/{}'.format(file), 
                names=['date', 'begin', 'high', 'low', 'end', 'compare', 'compare_rate', 'turnover'],
                parse_dates=['date'], 
                index_col=['date'], 
                date_parser=lambda date: datetime.datetime.strptime(date, '%y/%m/%d')).sort_index()
    return data
