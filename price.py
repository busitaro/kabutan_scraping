import csv
import time

from requests import get_html

base_url = 'https://kabutan.jp/stock/kabuka?code={code}&ashi=day&page={page}'
out_file = './price_{code}.csv'
sleep_time = 100


def get_price_chart_html(code):
    for page in range(1, 11):
        yield get_html(base_url.format(code=code, page=page))


def get_price_chart(soup):
    tr_list = soup.select('#stock_kabuka_table tr')[3:]
    td_list = [list(map(lambda x: x.text, tr.find_all(['td', 'th']))) for tr in tr_list]
    return td_list


def main():
    for code in range(from_code, 10000):
        time.sleep(sleep_time / 1000)
        out_data = []
        for soup in get_price_chart_html(code):
            try:
                if soup is not None:
                    out_data.extend(get_price_chart(soup))
            except Exception as e:
                print('type:{}'.format(str(type(e))))
                print('args:' + str(e.args))
        if len(out_data) > 0:
            out_data = sorted(out_data, key=lambda x: x[0])
            with open(out_file.format(code=code), 'a', encoding='utf_8', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerows(out_data)


if __name__ == '__main__':
    main()
