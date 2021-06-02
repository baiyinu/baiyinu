import urllib.request
from urllib import request,parse

# 编写好一个url，带上传送的数据，获取结果
url = 'http://httpbin.org/post'
dict = {
    'name' : 'Germey'
}
# header
data = bytes(parse.urlencode(dict), encoding='utf8')
req = request.Request(url=url, data=data, method='POST')
response = request.urlopen(req)
print(response.read().decode('utf-8'))

pattern = re.compile('<li.*?cover.*?href="(.*?)".*?title="(.*?)".*?more-meta.*?author">(.*?)</span>.*?year">(.*?)</span>.*?</li>', re.S)