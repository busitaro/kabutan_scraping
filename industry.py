import csv
import time

from requests import get_html

from setting.config import Config

base_url = 'https://kabutan.jp/stock/?code={code}'
out_file = 'industry.csv'
sleep_time = 100


def get_price_chart(soup):
    for tr in soup.select('#stock_kabuka_table tr'):
        td_list = list(map(lambda x: x.text, tr.find_all(['td', 'th'])))
        yield td_list[:4] + td_list[6:]


def get_sector(soup):
    return soup.select('#stockinfo_i2 a')[0].text


def main():
    config = Config()
    path_to_output = '{}/{}'.format(config.output_path(), out_file)
    with open(path_to_output, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for code in range(1300, 10000):
            time.sleep(sleep_time / 1000)
            soup = get_html(base_url.format(code=code))
            try:
                if soup is not None:
                    writer.writerow([code, get_sector(soup)])
            except Exception as e:
                print('type:{}'.format(str(type(e))))
                print('args:' + str(e.args))


if __name__ == '__main__':
    main()
