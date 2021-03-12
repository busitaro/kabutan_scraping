import sys
import datetime
import re
import pandas as pd

from input import input_data, input_business_day_file
from setting.config import Config


def get_days_with_no_data(
            check_data: dict, 
            business_day: pd.DataFrame, 
            begin_date: datetime.datetime, 
            end_date: datetime.datetime):
    """
    価格データと営業日データを照合し、
    価格データの欠損をチェックする

    Params
    --------
    check_date: dict
        チェック対象のデータ
        (key: ファイル名, value: 価格データ(pd.DataFrame))
    business_data: pd.DataFrame
        営業日データ
    begin_date: datetime.datetime
        チェック開始日
    end_date: datetime.datetime
        チェック終了日

    Returns
    ---------
    チェック結果: dict
        key: 銘柄コード, value: 欠損日のリスト
    """
    check_result = dict()
    check_business_day = business_day.loc[begin_date:end_date]

    for file_name, data in check_data.items():
        # ファイル名から、銘柄コードを取得
        code = re.sub('price_|.csv', '', file_name)
        # チェック対象営業日とデータをマージし、
        # データがNaNの日を抽出
        check_data = pd.merge(check_business_day.copy(), data, left_on='date', right_index=True, how='left')
        no_data_date = list(check_data[check_data['begin'].isna()].index)
        if len(no_data_date) > 0:
            check_result[code] = no_data_date

    return check_result


def main(file_path, begin_date, end_date):
    config = Config()
    check_data = input_data(config.output_path)
    business_day = input_business_day_file()
    for code, check_result in get_days_with_no_data(check_data, business_day, begin_date, end_date):
        print(code, check_result, sep=' => ')



if __name__ == '__main__':
    """
    Params
    --------
    1: data_file_path
    2: check_begin_date(yyyy-mm-dd)
    3: check_end_date(yyyy-mm-dd)
    """
    args = sys.argv
    if len(args) != 4:
        print('prameters are invalid')
    
    file_path = args[1]
    begin_date = datetime.datetime.strptime(args[2], '%Y-%m-%d')
    end_date = datetime.datetime.strptime(args[3], '%Y-%m-%d')
    main(file_path, begin_date, end_date)
