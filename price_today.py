import csv
import datetime
import time

from requests import get_html

from setting.config import Config

base_url = 'https://kabutan.jp/stock/kabuka?code={code}'
out_file =  'price_{code}.csv'
sleep_time = 100


def get_price_chart(soup):
    return list(map(lambda x: x.text, soup.select('#stock_kabuka_table tr')[1].find_all(['td', 'th'])))


def main():
    config = Config()
    today = datetime.date.today().strftime('%Y%m%d')
    for code in range(1300, 10000):
        time.sleep(sleep_time / 1000)
        soup = get_html(base_url.format(code=code))
        try:
            if soup is not None:
                path_to_output = '{}/{}'.format(config.output_path(), out_file.format(code=code))
                with open(path_to_output, 'a', encoding='utf_8', newline='') as f:
                    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                    writer.writerow(get_price_chart(soup))
        except Exception as e:
            print('type:{}'.format(str(type(e))))
            print('args:' + str(e.args))


if __name__ == '__main__':
    main()
