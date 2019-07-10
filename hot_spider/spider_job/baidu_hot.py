from datetime import datetime

import requests
from requests.exceptions import RequestException
import re

from hot_spider.models.models import HotSearch, TimeRank


def get_time():
    now = datetime.now()
    return now.strftime('%Y%m%d%H')
def get_one_bage(url):
    try:
        response = requests.get(url)
        response.encoding = 'gbk'
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


def pase_one_page(html):
    pattern = re.compile('"num-.*?">(\d+)</span>.*?href="(.*?)".*?href_top=".*?">(.*?)</a>'+
                         '.*?<td.*?href="(.*?)".*?href="(.*?)".*?href="(.*?)".*?"icon-.*?>(\d+)</span>'
                         ,re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield{
            'title': item[2],
            'type': 0,
            'url': item[1],
            'new_url': item[3],
            'image_url': item[4],
            'video_url': item[5],
            'count': item[6],
            'ranking': item[0]
        }


def write_to_database(content):
    for item in content:
        hot, created = HotSearch.get_or_create(title=item['title'],
                                               defaults={'type': 0, 'url': item['url'],
                                                         'describe': '', 'new_url': item['new_url'],
                                                         'image_url': item['image_url'], 'video_url': item['video_url']})

        # hot = HotSearch(title=item['title'], url=item['url'], type=0,
        #                 describe='', new_url=item['new_url'],
        #                 video_url=item['video_url'], image_url=item['image_url'])
        hot.save()
        rank = TimeRank(time=get_time(), ranking=item['ranking'],
                        hot_id=hot.id, count=item['count'])
        rank.save()





def main():
    url = 'http://top.baidu.com/buzz?b=1&fr=20811'
    html = get_one_bage(url)
    items = []
    for item in pase_one_page(html):
        items.append(item)
    write_to_database(items)



if __name__ == '__main__':
    main()