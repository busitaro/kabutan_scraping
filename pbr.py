import csv
import time

from requests import get_html

base_url = 'https://kabutan.jp/stock/kabuka?code={code}'
out_file = './pbr.csv'
sleep_time = 100


def get_pbr(soup):
    return soup.select('#stockinfo_i3 tr td')[1].text[:-1]


def main():
    with open(out_file, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for code in range(1300, 10000):
            time.sleep(sleep_time / 1000)
            soup = get_html(base_url.format(code=code))
            try:
                if soup is not None:
                    writer.writerow([code, get_pbr(soup)])
            except Exception as e:
                print('type:{}'.format(str(type(e))))
                print('args:' + str(e.args))


if __name__ == '__main__':
    main()
