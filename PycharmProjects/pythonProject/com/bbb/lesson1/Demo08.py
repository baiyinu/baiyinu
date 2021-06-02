import concurrent.futures
import re
from pyquery import PyQuery as pq
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from config import *
import pymongo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.PhantomJS()
wait = WebDriverWait(browser, 10)

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def serch():
    browser.get('https://www.taobao.com')
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )

        input.send_keys('美食')
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        return total.text
    except TimeoutException:
        return serch()

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('储存成功', result)
    except Exception:
        print('储存失败')
def next_page(page_number):
    input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
    input.clear()
    input.send_keys(page_number)
    submit.click()
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
    save_to_mongo(get_products())
def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist > div > div > div:nth-child(1) > div:nth-child(4)')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist > div > div > div:nth-child(1) > div:nth-child(4)').items()
    for item in items:
        product = {
            'img' : item.find('.pic .img').attr('src'),
            'price': item.find('.prcee').text()
        }
    return product

def main():
    total = serch()
    total = int(re.compile( '(\d+)' ).search(total).group(1))
    for i in range(1, total+1):
        next_page(i)

if __name__ == '__main__':
    main()