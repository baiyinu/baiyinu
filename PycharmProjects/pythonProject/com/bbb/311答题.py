import re
import time
from pyquery import PyQuery
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import requests


browser = webdriver.Firefox()
wait = WebDriverWait(browser, 30)
browser.get('http://eol.sdfmu.edu.cn/meol/index.do')

def register():
    click = wait.until(EC.element_to_be_clickable((By.ID, 'loginbtn')))
    click.click()
    username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#userName')))
    userpsw = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#passWord')))
    # user = input('输入学号：')
    # psw = input('输入密码：')
    user = '4119080016'
    psw = 'byp1101@'
    username.send_keys(user)
    userpsw.send_keys(psw)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#login > div.login-button > input'))).click()

    # serial_number = input('输入课程名称：')
    # click = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/div/div/div/div[3]/div[3]/div/div/div[2]/ul/li[16]/div[1]/a/img'))).click()
    windows = browser.current_window_handle
    browser.switch_to_window(windows[-1])
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#tmenu > li:nth-child(5) > a > span'))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#menu > ul.ul_493424 > li:nth-child(4) > a'))).click()

    time.sleep(10)

    # doc = PyQuery(browser.page_source)
    # item = doc.find('#body').text()
    while(1):
        doc = PyQuery(browser.page_source)
        print(doc.text())
        item = doc('#body').text()
        print(item)
        print(sou(item))
        input()





def sou(question):
    url = 'http://cx.icodef.com/wyn-nb?v=2'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Authorization': '',

    }
    data = {'question': question}
    response = requests.post(url, headers=headers, data=data)
    print(response.text)



def main():
    register()
if __name__ == '__main__':
    main()