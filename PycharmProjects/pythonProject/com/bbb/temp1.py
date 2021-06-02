import requests
import json
question = "中国共产党成立于"
url= 'http://cx.icodef.com/wyn-nb?v=2'
headers = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Authorization': '',

    }
data = {'question': question}
response = requests.post(url, headers=headers, data=data)
print(response.text)