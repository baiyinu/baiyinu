import re
import time
from pyquery import PyQuery

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


browse = webdriver.Firefox()    #定义一个浏览器
wait = WebDriverWait(browse, 30)   #设置等待，超时Time out


# 打开查询界面，开始查询
def seach():

    browse.get('https://s.wanfangdata.com.cn/advanced-search/paper')    #打开界面
    try:
        click = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[1]/div[2]/div[1]/span[2]')))                                    #定位元素专业检索
        inp = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div[1]/div[4]/div[2]/div[2]/div[3]/div[2]/div[1]/textarea')))     #输入框
        submit = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[1]/div[6]/span[1]')))                                          #检索按钮
        click.click()
        str = input('请输入查询内容：')    #获取查询内容
        inp.send_keys(str)              #查询内容上传到网页
        submit.click()                  #开始查询


    except TimeoutException:
        print('Time out')

def get_page():
    # 查询内容
    content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div:nth-child(8) > div > div.result-wrapper > div.list-wrapper > div.wf-list-container > div.top-content > div')))
    print(content.text)
    # 查询数据数量
    total_number = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div:nth-child(8) > div > div.result-wrapper > div.list-wrapper > div.wf-list-container > div.me-container.t-MT20.t-MB30.t-CLF > div.right-content > div > div > div.top-check-bar > span')))
    # total_number = int(re.compile(r'(\d+)').search(total_number.text).group(1))
    print(total_number.text)
    # 获取页码
    page_number = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div:nth-child(8) > div > div.result-wrapper > div.list-wrapper > div.wf-list-container > div.me-container.t-MT20.t-MB30.t-CLF > div.right-content > div > div > div.top-control-bar > div.right-bar > div.small-paginate > span.page-number')))
    page_number = int(re.compile(r'1 / (\d+)').search(page_number.text).group(1))
    # print(page_number)
    # 点击下一页
    click = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                   'body > div:nth-child(8) > div > div.result-wrapper > div.list-wrapper > div.wf-list-container > div.me-container.t-MT20.t-MB30.t-CLF > div.right-content > div > div > div.bottom-pagination > span.next')))
    result = []                         #用于存放结果
    if page_number < 2:
        result.append(parse_page())
        return result
    for i in range(1, page_number):

        result.append(parse_page())
        # print(parse_page())
        click.click()
    return result

# 解析当前界面
def parse_page():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                               'body > div:nth-child(8) > div > div.result-wrapper > div.list-wrapper > div.wf-list-container')))
    doc = PyQuery(browse.page_source)
    items = doc('.normal-list').items()
    for item in items:
        product = {
            '题目': item.find('.title').text(),
            '作者': item.find('.authors').text(),
            '期刊': item.find('.periodical-title').text(),
            # '卷期': item.find('').text()[-1]
        }
        yield product


def main():
    seach()
    for items in get_page():
        for item in items:
            print(item.items())

if __name__ == '__main__':
    main()