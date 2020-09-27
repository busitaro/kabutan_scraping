import csv
import sys

from input import input_data

file_path = '.\\'


def add_separator_to_path(path):
    if path[-1:] != '\\':
        path = path + '\\'
    return path


def main(file_path):
    for file, data in input_data(file_path).items():
        data = data.drop_duplicates()
        data.to_csv(file_path + file, encoding='utf-8', quoting=csv.QUOTE_ALL, header=False, date_format='%y/%m/%d')


if __name__ == '__main__':
    args = sys.argv
    if len(args) >= 2:
        file_path = args[1]
    main(add_separator_to_path(file_path))
