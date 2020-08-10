import csv
import datetime
import time

from requests import get_html

base_url = 'https://kabutan.jp/stock/kabuka?code={code}'
out_file = './price_{code}_{date}.csv'
sleep_time = 100


def get_price_chart(soup):
    for tr in soup.select('#stock_kabuka_table tr')[:2]:
        td_list = list(map(lambda x: x.text, tr.find_all(['td', 'th'])))
        yield td_list


def main():
    today = datetime.date.today().strftime('%Y%m%d')
    for code in range(1300, 10000):
        time.sleep(sleep_time / 1000)
        soup = get_html(base_url.format(code=code))
        try:
            if soup is not None:
                with open(out_file.format(code=code, date=today), 'w') as f:
                    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                    for row in get_price_chart(soup):
                        writer.writerow(row)
        except Exception as e:
            print('type:{}'.format(str(type(e))))
            print('args:' + str(e.args))


if __name__ == '__main__':
    main()
