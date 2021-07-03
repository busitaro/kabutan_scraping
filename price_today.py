import csv
import datetime
import time

from requests import get_html

from setting.config import Config

base_url = 'https://kabutan.jp/stock/kabuka?code={code}'
out_file =  'price_{code}.csv'
sleep_time = 100


def get_price_chart(soup):
    price_table_tr = soup.select('#stock_kabuka_table .stock_kabuka0 tr')
    if len(price_table_tr) <= 1:
        return
    else:
        return list(map(lambda x: x.text, price_table_tr[1].find_all(['td', 'th'])))


def get_price_data(code: str) -> list: 
    """
    WEBから価格データを取得する

    Params
    --------
    code: str
        取得対象の銘柄コード

    Returns
    ---------
    list:
        取得した価格データ
    """
    soup = get_html(base_url.format(code=code))
    if soup is not None:
        data = get_price_chart(soup)
        return data
    else:
        return


def output_price_data(code: str, data: list):
    """
    データをファイル出力する

    Params
    --------
    code: str
        銘柄コード
    data: list
        出力するデータ
    """
    config = Config()
    path_to_output = '{}/{}'.format(config.output_path, out_file.format(code=code))
    with open(path_to_output, 'a', encoding='utf_8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(data)


def price_today(code: str):
    """
    指定された銘柄のデータ取得、出力を行う

    Params
    --------
    code: str
        銘柄コード
    """
    try:
        data = get_price_data(code)
        if data is not None and len(data) > 0:
            output_price_data(code, data)
    except Exception as e:
        print('type:{}'.format(str(type(e))))
        print('args:' + str(e.args))


def main():
    for code in range(1300, 10000):
        time.sleep(sleep_time / 1000)
        price_today(str(code))


if __name__ == '__main__':
    main()
