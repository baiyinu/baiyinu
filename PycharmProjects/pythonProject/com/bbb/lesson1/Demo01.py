import requests
from requests.exceptions import RequestException
import re

def get_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None

    except RequestException:
        return None
def parse_page(html):
    pattrn = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src"(.*?)".*?name"><a')

def main():
    url = 'https://maoyan.com/board/4'
    html = get_page(url)
    print(html)

if __name__ == '__main__':
    main()

