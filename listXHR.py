# requests more naver news

import Article
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
    for i in range(k):
        data = {"page": str(i)}
        r = requests.post(url, headers=headers, data=data)
        data = json.loads(r.text)
        #with open("NewsList_0507" + "/" + str(i) + ".txt", "w") as f:
        #    f.write(r.text)
        for j in range(12):
                article = Article.NewsArticle()
                article.ArticleID = data["message"]["itemList"][j]["articleId"]
                article.ArticleTitle = data["message"]["itemList"][j]["title"]
                article.ArticleDate = data["message"]["itemList"][j]["standardFullDate"]
                article.ThumbnailImageURL = str(data["message"]["itemList"][j]["imageUrl"])
                article.Video = data["message"]["itemList"][j]["videoType"]
                article.Link = "http://m.news.naver.com" + data["message"]["itemList"][j]["linkUrl"]
                article.get_contents()
                article.log()
                print(" ")
        print(i)

main(1)