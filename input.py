import datetime
import os
import re
import pandas as pd

business_day_file='file/business_day.csv'
exclude_file = 'file/exclude.lst'


def input_data(dir_path, exclude=True):
    data = dict()
    if exclude:
        exclude_list = input_exclude_list()
    for file in os.listdir(dir_path):
        if file.startswith('price'):
            if exclude:
                if re.sub('price_|.csv', '', file) in exclude_list:
                    continue
            try:
                data[file] = \
                    pd.read_csv(
                        '{}/{}'.format(dir_path, file), 
                        names=['date', 'begin', 'high', 'low', 'end', 'compare', 'compare_rate', 'turnover'],
                        parse_dates=['date'], 
                        index_col=['date'], 
                        date_parser=lambda date: datetime.datetime.strptime(date, '%y/%m/%d')).sort_index()
            except:
                print('input error file: {}'.format(file))
    return data


def input_trade_data(dir_path, exclude=True):
    data = dict()
    if exclude:
        exclude_list = input_exclude_list()
    for file in os.listdir(dir_path):
        if file.startswith('trade'):
            if exclude:
                if re.sub('trade_|.csv', '', file) in exclude_list:
                    continue
            try:
                data[file] = \
                    pd.read_csv(
                        '{}/{}'.format(dir_path, file), 
                        names=['date', 'turnover', 'trading_total_price', 'vwap', 'trading_count', 'need_price', 'unit', 'market_capitalization', 'num_of_stocks'],
                        parse_dates=['date'], 
                        index_col=['date'], 
                        date_parser=lambda date: datetime.datetime.strptime(date, '%Y-%m-%d')
                    ).sort_index()
            except:
                print('input error file: {}'.format(file))
    return data


def input_business_day_file(file_path=business_day_file) -> pd.DataFrame:
    """
    営業日ファイルを読み込む

    Params
    --------
    file_path
        営業日ファイルのパス

    Returns
    ---------
    pd.DataFrame
        営業日ファイルを読み込んだ結果
        (index: 日付、 col1: True=>営業日/False=>非営業日
    """
    file = pd.read_csv(
                file_path, 
                names=['date', 'business'],
                parse_dates=['date'], 
                index_col=['date'], 
                date_parser=lambda date: datetime.datetime.strptime(date, '%Y/%m/%d'), 
                thousands=',').sort_index()
    return file


def input_exclude_list():
    with open(exclude_file, 'r') as f:
        exclude_list = [code.replace('\n', '') for code in f.readlines()]
    return exclude_list
