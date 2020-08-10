import urllib.request

from bs4 import BeautifulSoup


max_retry = 5


def get_html(url, retry_cnt=0):
    if retry_cnt > max_retry:
        print('URL is invalid => {url}'.format(url=url))
        return
    try:
        html = urllib.request.urlopen(url, timeout=100).read()
        if html is None:
            get_html(url, retry_cnt + 1)
        soup = BeautifulSoup(html, 'lxml')
        
        if not is_exists_code(soup):
            return
        elif not is_listing(soup):
            return
        return soup
    except Exception:
        get_html(url, retry_cnt + 1)


def is_exists_code(soup):
    return soup.select('.topicpath span')[1].text[:1] != '('


def is_listing(soup):
    return len(soup.select('.si_i1_2 img')) == 0
