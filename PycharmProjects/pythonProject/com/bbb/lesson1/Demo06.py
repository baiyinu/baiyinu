import requests
import re
from selenium import webdriver
from requests import RequestException


def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    try:
        html = requests.get('https://book.douban.com/', headers=headers)
        if html.status_code == 200:
            return html.text
        return  None
    except RequestException:
        return None

def parse_page(response):
    pattern = re.compile(r'<dd>.*?title="(.*?)".*?<img data-src="(.*?)".*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>', re.S)
    items = re.findall(pattern, response)
    for item in items:
        yield {
            '电影名': item[0],
            'image': item[2],
            'star': item[3],
            '上映时间': item[4]
        }

def main():
    url = 'https://maoyan.com/board/4'
    response = get_page(url)

    print(parse_page(response))



if __name__ == '__main__':
    main()