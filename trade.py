import csv
import time

from requests import get_html as g_html

from setting.config import Config

base_url = 'https://kabutan.jp/stock/?code={code}'
out_file = 'trade_{code}.csv'
sleep_time = 100


def get_html(code):
    return g_html(base_url.format(code=code))


def get_data(code):
    out_data = []
    soup = get_html(code)
    try:
        if soup is not None:
            out_data.append(soup.find(id='kobetsu_left').find_all('time')[1]['datetime'])
            out_data.extend([td.text for td in soup.find(id='kobetsu_left').find_all('table')[1].select('td')])
    except Exception as e:
        print('----- code: {} -----'.format(code=code))
        print('type:{}'.format(str(type(e))))
        print('args:' + str(e.args))
    return out_data


def output(code, data):
    config = Config()
    path_to_output = '{}/{}'.format(config.output_path, out_file.format(code=code))
    with open(path_to_output, 'a', encoding='utf_8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(data)


def main():
    for code in range(1300, 10000):
        time.sleep(sleep_time / 1000)
        out_data = get_data(code)
        if len(out_data) != 0 and out_data[0] != '':
            output(code, out_data)


if __name__ == '__main__':
    main()
