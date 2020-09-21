import csv
import sys
import os
import datetime
import pandas as pd

file_path = '.\\'


def input_file(file_path):
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


def add_separator_to_path(path):
    if path[-1:] != '\\':
        path = path + '\\'
    return path


def main(file_path):
    for file, data in input_file(file_path).items():
        data.to_csv(file_path + file, encoding='utf-8', quoting=csv.QUOTE_ALL, header=False, date_format='%y/%m/%d')


if __name__ == '__main__':
    args = sys.argv
    if len(args) >= 2:
        file_path = args[1]
    main(add_separator_to_path(file_path))
