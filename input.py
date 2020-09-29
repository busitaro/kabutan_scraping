import datetime
import os
import pandas as pd

business_day_file='.\\file\\business_day.csv'


def input_data(file_path):
    data = dict()
    for file in os.listdir(file_path):
        data[file] = \
            pd.read_csv(
                '{}/{}'.format(file_path, file), 
                names=['date', 'begin', 'high', 'low', 'end', 'compare', 'compare_rate', 'turnover'],
                parse_dates=['date'], 
                index_col=['date'], 
                date_parser=lambda date: datetime.datetime.strptime(date, '%y/%m/%d')).sort_index()
    return data


def input_business_day_file(file_path=business_day_file):
    file = pd.read_csv(
                file_path, 
                names=['date', 'business'],
                parse_dates=['date'], 
                index_col=['date'], 
                date_parser=lambda date: datetime.datetime.strptime(date, '%Y/%m/%d'), 
                thousands=',').sort_index()
    return file
