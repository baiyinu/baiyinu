import requests
import os
from PIL import Image
from aip import AipOcr
import json


def get_screenshot():
    # 截屏
    os.system('adb shell screencap -p /sdcard/image.png')
    os.system('adb pull /sdcard/image.png')


def get_word_by_img():
    # 文字识别
    APP_ID = '16227766'
    API_KEY = 'FgubvnxtReF32vR4jGsS4FY4'
    SECRET_KEY = 'R5YbhWyY2NMF102wRZTwVm9U4hjeAwQG'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    i = open(r'/home/bbb/PycharmProjects/pythonProject/com/bbb/image.png', 'rb')
    img = i.read()
    img_res = client.basicGeneral(img)
    return img_res


def baidu(question, answers):
    # 进行百度
    url = 'https://www.baidu.com/s'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    data = {
        'wd': question
    }
    res = requests.get(url=url, params=data, headers=headers)
    res.encoding = 'utf-8'
    html = res.text
    for i in range(len(answers)):
        answers[i] = (html.count(answers[i]), answers[i], i)
    answers.sort(reverse=True)
    return answers

def seach(question):
    url = 'http://cx.icodef.com/wyn-nb?v=2'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Authorization': '',

    }
    data = {'question': question}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.text
    else:
        return None



def run():
    while True:
        input("回车答题")
        get_screenshot()
        img = Image.open('/home/bbb/PycharmProjects/pythonProject/com/bbb/image.png')
        title_img = img.crop((80, 500, 1000, 880))
        answers_img = img.crop((80, 960, 1000, 1720))
        new_img = Image.new('RGBA', (920, 1140))
        new_img.paste(title_img, (0, 0, 920, 380))
        new_img.paste(answers_img, (0, 380, 920, 1140))
        new_img.save('new_img_fb.png')

        info = get_word_by_img()
        answers = [x['words'] for x in info['words_result']]
        # print(answers)
        question = ''.join([x['words'] for x in info['words_result']])
        # print(question)
        result = json.loads(seach(question))
        if result:
            code = result['code']
            answer = result['data']
            if code == 1:

                print(question)
                print(answer)
            else:
                print('无答案')
        else:
            print('time out')

if __name__ == '__main__':
    run()