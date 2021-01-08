import datetime
import os
import re
import pandas as pd

business_day_file='file/business_day.csv'
exclude_file = 'file/exclude.lst'


def input_data(file_path, exclude=True):
    data = dict()
    if exclude:
        with open(exclude_file, 'r') as f:
            exclude_list = [code.replace('\n', '') for code in f.readlines()]
    for file in os.listdir(file_path):
        if file.startswith('price'):
            if exclude:
                if re.sub('price_|.csv', '', file) in exclude_list:
                    continue
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
