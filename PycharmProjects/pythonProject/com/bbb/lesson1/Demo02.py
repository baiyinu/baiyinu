import json

import requests
from urllib.parse import urlencode
import re

# 获取索引页
def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3
    }
    url = 'https://www.toutiao.com/search/?' + urlencode(data)
    headers = {
        'User - Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
                   }
    response = requests.get(url, headers= headers)
    if response.status_code == 200:
        return response.text
    return None

def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def main():
    html = get_page_index(0, '街拍')
    for url in parse_page_index(html):
         print(url)



if __name__ == '__main__':
    main()