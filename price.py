import csv
import sys
import time

from requests import get_html

base_url = 'https://kabutan.jp/stock/kabuka?code={code}&ashi=day&page={page}'
out_file = './price_{code}.csv'
sleep_time = 100


def get_price_chart_html(code):
    for page in range(1, 11):
        yield get_html(base_url.format(code=code, page=page))


def get_price_chart(soup):
    for tr in soup.select('#stock_kabuka_table tr')[3:]:
        td_list = list(map(lambda x: x.text, tr.find_all(['td', 'th'])))
        yield td_list


def main(from_code=1300):
    for code in range(from_code, 10000):
        time.sleep(sleep_time / 1000)
        for soup in get_price_chart_html(code):
            try:
                if soup is not None:
                    with open(out_file.format(code=code), 'a') as f:
                        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                        for row in get_price_chart(soup):
                            writer.writerow(row)
            except Exception as e:
                print('type:{}'.format(str(type(e))))
                print('args:' + str(e.args))


if __name__ == '__main__':
    args = sys.argv
    if len(args) >= 2:
        from_code = int(args[1])
    else:
        from_code = 1
    main(from_code)
