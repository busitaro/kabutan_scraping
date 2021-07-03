import csv
import datetime
import sys
import time

from requests import get_html

from setting.config import Config

base_url = 'https://kabutan.jp/stock/kabuka?code={code}&ashi=day&page={page}'
out_file = 'price_{code}.csv'
sleep_time = 100


def get_price_chart_html(code):
    for page in range(1, 11):
        yield get_html(base_url.format(code=code, page=page))


def get_price_chart(soup):
    tr_list = soup.select('#stock_kabuka_table tr')[3:]
    td_list = [list(map(lambda x: x.text, tr.find_all(['td', 'th']))) for tr in tr_list]
    return td_list


def format_date(yyyymmdd: str):
    dt = datetime.datetime.strptime(yyyymmdd, '%Y%m%d')
    return dt.strftime('%y%m%d')


def get_data(code, from_date, end_date):
    out_data = []
    for soup in get_price_chart_html(code):
        try:
            if soup is not None:
                price_data = list(filter(lambda x: int(x[0].replace('/', '')) >= int(from_date), get_price_chart(soup)))
                if len(price_data) == 0:
                    break
                price_data = list(filter(lambda x: int(x[0].replace('/', '')) <= int(end_date), price_data))
                out_data.extend(price_data)
            else:
                break
        except Exception as e:
            print('type:{}'.format(str(type(e))))
            print('args:' + str(e.args))
    return out_data


def output(code, data):
    data = sorted(data, key=lambda x: x[0])
    config = Config()
    path_to_output = '{}/{}'.format(config.output_path, out_file.format(code=code))
    with open(path_to_output, 'a', encoding='utf_8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(data)


def main(code, from_date, end_date):
    if code != '':
        out_data = get_data(code, from_date, end_date)
        if len(out_data) > 0:
            output(code, out_data)
    else:
        for code in range(1300, 10000):
            time.sleep(sleep_time / 1000)
            out_data = get_data(code, from_date, end_date)
            if len(out_data) > 0:
                output(code, out_data)


if __name__ == '__main__':
    args = sys.argv

    code = ''
    from_date = 1
    end_date = 99999999

    if len(args) >= 2:
        code = args[1].strip()
    if len(args) >= 3:
        from_date = format_date(args[2])
    if len(args) >= 4:
        end_date = format_date(args[3])

    main(code, from_date, end_date)
