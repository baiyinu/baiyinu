import json
import re
import time
from urllib.parse import urlencode

import pymongo as pymongo
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from requests import RequestException
from config import *

client = pymongo.MongoClient(MONGO_URL)

db = client(MONGO_DB)

def get_page_index(offset):
    data = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': 1618731770300,
        '_signature': '_02B4Z6wo00d01aAlivwAAIDCXT.4J.CtBEGgAY5AAAhzpUeOObYaBZSUjycentlYcbPoKqcHc7htozvvkj-uwTN0uPoLR.GkKJz.kkZ3PDE-aPbKqhCKi8fdOqMxJ4EV0E7FuvN-qaZOd5mE9c'
        }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(data)
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求出错')
        return None

def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_datail(url):
    try:
        browser = webdriver.Firefox()
        browser.get(url)

        title = browser.find_element_by_xpath(r'/html/head/title')
        print(title)
    finally:
        browser.close()


def parse_page_datail(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('title')
    image_patter = re.compile(r'class="image-item".*?<img src="(.*?)">', re.S)
    data = re.search(image_patter, html)
    print(data)


def main():
    html = get_page_index(0)
    for url in parse_page_index(html):
        if url:
            html = get_page_datail(url)
            print(html)
            parse_page_datail(html)


if __name__ == '__main__':
    main()