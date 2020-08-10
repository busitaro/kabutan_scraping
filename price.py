import csv
import datetime
import time
import urllib.request

from bs4 import BeautifulSoup

base_url = 'https://kabutan.jp/stock/kabuka?code={code}'
out_file = './{code}_{date}_price.csv'
max_retry = 5
sleep_time = 100


def get_html(code, retry_cnt=0):
    url = base_url.format(code=code)
    if retry_cnt > max_retry:
        print('URL is invalid => {url}'.format(url=url))
        return
    try:
        html = urllib.request.urlopen(url, timeout=100).read()
        if html is None:
            get_html(code, retry_cnt + 1)
        soup = BeautifulSoup(html, 'lxml')
        
        if not is_exists_code(soup):
            return
        elif not is_valid_html(soup):
            get_html(code, retry_cnt + 1)
        return soup
    except Exception:
        get_html(code, retry_cnt + 1)


def is_exists_code(soup):
    if soup.select('.topicpath span')[1].text[:1] == '(':
        return False
    else:
        return True


def is_valid_html(soup):
    if len(soup.select('#stock_kabuka_table')):
        return True
    else:
        return False


def get_price_chart(soup):
    for tr in soup.select('#stock_kabuka_table tr'):
        td_list = list(map(lambda x: x.text, tr.find_all(['td', 'th'])))
        yield td_list


def main():
    today = datetime.date.today().strftime('%Y%m%d')
    for code in range(1300, 10000):
        time.sleep(sleep_time / 1000)
        soup = get_html(code)
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
