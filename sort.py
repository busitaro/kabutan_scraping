import csv
import sys

from input import input_data
from setting.config import Config


def main():
    config = Config()
    file_path = config.output_path()

    for file, data in input_data(file_path).items():
        data = data.groupby(level=0).last()
        print('{}/{}'.format(file_path, file))
        data.to_csv('{}/{}'.format(file_path, file), encoding='utf-8', quoting=csv.QUOTE_ALL, header=False, date_format='%y/%m/%d')


if __name__ == '__main__':
    main()
