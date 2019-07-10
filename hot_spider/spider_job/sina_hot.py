from bs4 import BeautifulSoup
import requests

from requests import RequestException


def get_one_bage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:

            return response.text
        else:
            return None
    except RequestException:
        return None


def get_data_from_html(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('tbody')
    print(table)
    for tr in  table.find_all('tr'):
        yield {
            'index': tr.td.string,
            'title':tr.find("a").string,
            'href':tr.find("a")['href'],
            'type':tr.find("td",attrs={"class": "td-03"}).string,
            'hot_num': '' if tr.find("span")== None  else tr.find("span").string
        }


def class_is_first(tag):
    if tag.has_attr('class'):
        return tag['class'] == ['first']
    return False

def main():
    url = 'https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6'
    html = get_one_bage(url)
    for item in get_data_from_html(html):
        print(item)
