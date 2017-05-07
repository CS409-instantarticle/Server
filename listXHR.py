
# requests more naver news

import json
import requests
import time

url = "http://m.news.naver.com/mainNews/moreMainNews.json"

headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'm.news.naver.com',
        'Origin': 'http://m.news.naver.com',
        'Referer': 'http://m.news.naver.com/',
        'X-Requested-With': 'XMLHttpRequest'
}

data = {#"articleId": "0000026799",
        #"officeId" : "353",
        #"pageSize": "12",
        "page" : 1,
        #"itemId": "2580052"
}

'''
# How to use

r = requests.post(url, headers=headers, data=data)
data = json.loads(r.text)
print(data)
'''

def main(k):
    for i in range(1, 420):
        data = {"page": str(i)}
        r = requests.post(url, headers=headers, data=data)
        data = json.loads(r.text)
        #with open("NewsList_0507" + "/" + str(i) + ".txt", "w") as f:
        #    f.write(r.text)
        #print(data)
        #print(i)
        return data


