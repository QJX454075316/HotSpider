from datetime import datetime

from bs4 import BeautifulSoup
import requests

from requests import RequestException

from models.models import HotSearch, TimeRank

def get_time():
    now = datetime.now()
    return now.strftime('%Y%m%d%H')


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
            'hot_num': 0 if tr.find("span")== None  else tr.find("span").string
        }


def write_to_database(item):
    hot, created = HotSearch.get_or_create(title=item['title'],
                                           defaults={'type': 1, 'url': item['href'],
                                                     'describe': '', 'new_url': '',
                                                     'image_url': '', 'video_url': ''})

    # hot = HotSearch(title=item['title'], url=item['url'], type=0,
    #                 describe='', new_url=item['new_url'],
    #                 video_url=item['video_url'], image_url=item['image_url'])
    hot.save()
    rank = TimeRank(time=get_time(), ranking=item['index'],
                    hot_id=hot.id, count=item['hot_num'])
    rank.save()


def sina_main_job():
    url = 'https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6'
    html = get_one_bage(url)
    for item in get_data_from_html(html):
        write_to_database(item)

