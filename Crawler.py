
# coding: utf-8

# In[1]:


# Article Crawler by Section
import requests 
import json
import sqlite3
import pickle 
import urllib
import time
from bs4 import BeautifulSoup as BS
from timeit import default_timer as timer
from multiprocessing import Process
import random

# Constants - Section ID
sectionId_Politics = 100
sectionId_Economy = 101
sectionId_Society = 102
sectionId_IT = 105
sectionId_Life = 103
sectionId_World = 104

section = {
    '정치' : sectionId_Politics,
    '경제' : sectionId_Economy,
    '사회' : sectionId_Society,
    'IT'   : sectionId_IT,
    '생활' : sectionId_Life,
    '세계' : sectionId_World
}

dbName = {
    '정치' : "article_politics",
    '경제' : "article_economy",
    '사회' : "article_society",
    'IT'   : "article_it",
    '생활' : "article_life",
    '세계' : "article_world"
}


# In[2]:


# 데이터베이스 초기화

conn_all = sqlite3.connect("article_all.db", isolation_level=None)
conn_politics = sqlite3.connect("article_politics.db", isolation_level=None)
conn_economy = sqlite3.connect("article_economy.db", isolation_level=None)
conn_society = sqlite3.connect("article_society.db", isolation_level=None)
conn_it = sqlite3.connect("article_it.db", isolation_level=None)
conn_life = sqlite3.connect("article_life.db", isolation_level=None)
conn_world = sqlite3.connect("article_world.db", isolation_level=None)

c_all = conn_all.cursor()
c_politics = conn_politics.cursor()
c_economy = conn_economy.cursor()
c_society = conn_society.cursor()
c_it = conn_it.cursor()
c_life = conn_life.cursor()
c_world = conn_world.cursor()

c_all.execute('drop table if exists article_all;')
c_politics.execute('drop table if exists article_politics;')
c_economy.execute('drop table if exists article_economy;')
c_society.execute('drop table if exists article_society;')
c_it.execute('drop table if exists article_it;')
c_life.execute('drop table if exists article_life;')
c_world.execute('drop table if exists article_world;')

table_scheme = '''(
        idx INTEGER PRIMARY KEY AUTOINCREMENT,
        itemid text NOT NULL UNIQUE,
        json text
)
'''

c_all.execute('''create table if not exists article_all %s;''' % table_scheme);
c_politics.execute('''create table if not exists article_politics %s;''' % table_scheme);
c_economy.execute('''create table if not exists article_economy %s;''' % table_scheme);
c_society.execute('''create table if not exists article_society %s;''' % table_scheme);
c_it.execute('''create table if not exists article_it %s;''' % table_scheme);
c_life.execute('''create table if not exists article_life %s;''' % table_scheme);
c_world.execute('''create table if not exists article_world %s;''' % table_scheme);

conn = {
    "article_all" : conn_all,
    "article_politics" : conn_politics,
    "article_economy" : conn_economy,
    "article_society" : conn_society,
    "article_it" : conn_it,
    "article_life" : conn_life,
    "article_world" : conn_world
}


c = {
    "article_all" : c_all,
    "article_politics" : c_politics,
    "article_economy" : c_economy,
    "article_society" : c_society,
    "article_it" : c_it,
    "article_life" : c_life,
    "article_world" : c_world
}

for x in conn.values():
    x.commit()


# In[3]:


# db 조작 명령어

def insert_article(tablename, itemid, json):
    # dict 안의 특수기호로 인해 바로 저장 불가능
    pdata = pickle.dumps(json, pickle.HIGHEST_PROTOCOL)
    cnt = 0
    while True:
        
        try:
            con = conn[tablename]
            con.execute('insert into %s (itemid, json) values (?, :data)' % tablename, (itemid, sqlite3.Binary(pdata)))
            #con.commit()
            break
            
        except sqlite3.OperationalError:
            if cnt > 5: break
            print("rest %s" % itemid)
            time.sleep(0.002 * random.randint(1, 5))
            cnt += 1
            
        except sqlite3.IntegrityError:
            print("skip %s" % itemid)
            break
    return


def select_article(tablename, limit):
    cur = c[tablename]
    cur.execute("select idx, itemid, json from %s order by idx desc limit %s " % (tablename, limit))
    return [(row[0], row[1], pickle.loads(row[2])) for row in cur]

'''
#test
insert_article("article_all", '1233', "{'asdf' : 'asdf\"asdfasdf\"'}")
insert_article("article_all", '1234', "{'asdf' : 'asdf\"asdfasdf\"'}")
insert_article("article_all", '1235', "{'asdf' : 'asdf\"asdfasdf\"'}")
insert_article("article_all", '1236', "{'asdf' : 'asdf\"asdfasdf\"'}")
insert_article("article_all", '1237', "{'asdf' : 'asdf\"asdfasdf\"'}")
print(select_article('article_all', 3))
c.execute("DELETE FROM article_all where 1 > 0;")
conn.commit()
'''


# In[4]:


"""
s = timer()
for i in range(101, 300):
    insert_article("article_all", str(i), "{'asdf' : 'asdf\"asdfasdf\"'}")
e = timer()

print(e - s)

s = timer()
print(select_article("article_all", 40))
e = timer()
print(e - s)
"""


# In[5]:


class NewsArticle:
    ArticleID = 0
    itemId = None
    ArticleTitle = None
    SectionName = None
    ArticleDate = None
    ThumbnailImageURL = None
    Video = False
    Link = None
    Press = None
    Raw_contents = None
    Contents = []

    # 이니셜라이저 : 각 기사별 json 받아서 데이터 타입에 맞게 저장
    def __init__(self, json):
        self.itemId = json["itemId"]
        self.ArticleID = json["articleId"]
        self.ArticleTitle = json["title"]
        self.ArticleDate = json["standardFullDate"] if 'standardFullDate' in json.keys() else None
        self.ThumbnailImageURL = str(json["imageUrl"])
        self.Video = json["videoType"]
        self.Press = json["officeName"]
        self.Link = "http://m.news.naver.com" + json["linkUrl"]
        self.SectionName = (
            json["sectionName"] if json["sectionName"] else None)
        self.get_contents()
        return
    
    
    # json 스트링 리턴
    def __str__(self):
        d = dict()
        d["ArticleID"] = str(self.ArticleID)
        d["ArticleTitle"] = str(self.ArticleTitle)
        d["SectionName"] = str(self.SectionName)
        d["ArticleDate"] = str(self.ArticleDate)
        d["Press"] = str(self.Press)
        d["ThumbnailImageURL"] = str(self.ThumbnailImageURL)
        d["Video"] = str(self.Video)
        d["Link"] = str(self.Link)
        d["Contents"] = (self.Contents)
        return str(d)
    
    
    # 컨텐츠 내용 파싱
    def get_contents(self):
        #print(self.ArticleTitle)
        texts = get_text(self.Link)
        self.Raw_contents = texts
        self.Contents = jsonify_content(texts)
        return
      
    '''
    
    # 파일 이름 저장 : 날짜 및 아티클 ID 기준
    def getFileName(self):
        fileName = "%s%s" % \
            (self.ArticleDate \
             .replace(":", "") \
             .replace("-", "") \
             .replace(" ", ""), 
             self.ArticleID)
        return fileName
        
        
    # 파일로 기록
    def write(self):
        fileName = self.getFileName()
        directory = "articles/%s" % fileName

        try:
            f = open(directory, "r")
        except IOError:
            if self.SectionName:
                print(self.SectionName)
                with open("articles/" + self.SectionName + fileName, "w") as f:
                    f.write(str(self))
            with open(directory, "w") as f:
                f.write(str(self))
            return
        # if reached : file exists
        raise IOError    
    '''


# In[6]:


# get_text : URL(str) ->> BS element
def get_text(URL):
    source_code_from_URL = str(urllib.request.urlopen(URL).read(), "utf-8").replace("<br>", "<br/>").replace("<br/><br/>", "<br/>")
    soup = BS(source_code_from_URL, 'html.parser')
    result = soup.find_all('div', id="dic_area")

    # entertain 뉴스를 레퍼런스로 하는 경우 별도의 핸들링 필요
    if not result:
        #print(URL)
        source_code_from_URL = str(urllib.request.urlopen(
            URL.replace("m.news.naver.com", "m.entertain.naver.com")).read(), "utf-8").replace("<br>", "<br/>").replace("<br/><br/>", "<br/>")
        soup = BS(source_code_from_URL, 'html.parser')
        result = soup.find_all('div', id="contentArea")
    
    return result[0]


# In[7]:


# BS contents ->>  [indexed dictionary, ...]
def jsonify_content(content):

    # BS.contents는 html 태그 안의 모든 first child를 리스트로 반환
    # 태그가 없어도 무방하므로 본문 내용까지 별도의 child로 리턴됨
    # 기사 앞뒤의 빈 칸(탭, 줄바꿈 기호 등)을 잘라내고 br 태그를 제거함
    content_list = content.contents
    x = list(filter(lambda s : s != "<br/>", map(lambda s: str(s).strip(), content_list)))

    # 각 object에 기사 요소의 배치 순서를 지시
    index = 0

    # json_list에 각 기사 요소를 순서대로 담아 리턴

    json_list = []
    # 텍스트 타입에 따라 분류
    # type : text, video, image, link
    for i in x:

        # 잘못 나온 놈은 걸러야 한다. 인덱스 추가 안하고 다음 요소 탐색
        if i == "":
            continue

        # 여기부턴 어쨌든 요소에 속함.
        # HTML 태그가 하나도 없으면 텍스트로 분류
        if not "<" in i:
            json_list.append({'ArticleIndex': index, "ArticleType": "text", 'content' : i})

        # 태그가 있는 요소들은 다음과 같이 분류함:
        else:
            bs = BS(i, 'html.parser')

            # 비디오 태그 : To Be Implemented
            if "<iframe" in i:
                video_url = bs.find('iframe').get('src')
                json_list.append({'ArticleIndex': index, "ArticleType": "text", 'content': video_url})

            elif "video_area" in i:
                #print(i)
                json_list.append({'ArticleIndex': index, "ArticleType": "text", 
                                  'content': "http://news.video.p.rmcnmv.naver.com/owfs_rmc/read/NEWS_2017_05_26_3/531C05F3C304F34C0F330E6E936E1FC3388_muploader_b_480P_854_1024_128.mp4?_lsu_sa_=632577fcc1be6046fdda357b66c57bba4ecf3f1831089f0633875ec1c74a3f2570240aed61357008709b3a129034fbc5effbc03b5726a5f16d6f884f367d5fa70774723c3e1698cc965eedfef0ec4a5a"})
                #video_url = bs.find('video').get('data-src')
                #json_list.append({'ArticleIndex': index, "ArticleType": "video", 'content': video_url})

            # 이미지 태그 : 대부분 span으로 묶여 있음. 사진과 태그 포함
            # 다만 다른 형식에 span이 사용될 수 있으므로 img를 이용함
            elif "<img" in i:
                #print('image')
                img_url = bs.find('img').get('data-src')
                img_tag = bs.find('em', class_='img_desc')
                # 이미지 태그가 없으면 빈 스트링을 저장함.
                if img_tag: img_tag = img_tag.text
                else: img_tag = ""
                json_list.append({'ArticleIndex': index, "ArticleType": "image", 'content': img_url, 'tag' : img_tag})


            # 링크 태그 : a 안에 들어 있음
            # 네이버 기사는 본문 안에 링크 삽입 잘 안하므로 a 안의 요소만 따도 무방
            elif "<a" in i:
                link_url = bs.find('a').get('href')
                link_text = bs.find('a').text
                json_list.append({'ArticleIndex': index, "ArticleType": "link", 'url': link_url, 'content': link_text})

            # 소제목 태그 : strong, em 등의 텍스트 요소를 포함함
            elif any(["<font" in i, "<strong" in i, "<b" in i]):
                json_list.append({'ArticleIndex': index, "ArticleType": "strapline", 'content': bs.text})

            # 가끔 텍스트에 꺾쇠를 집어넣는 똥같은 언론사들이 있음
            # 문과가 또...
            # 이 경우는 텍스트로 분류
            else:
                json_list.append({'ArticleIndex': index, "ArticleType": "text", 'content': bs.text})

        #print(index)
        index += 1
    return json_list


# In[8]:


# request first 12 extlements
# sectionId : int --> [list-of Articles]
def requestBySection(sectionName, limit=10, log=False):
    
    assert type(limit) == int
    assert limit >= 1
    
    sectionId = section[sectionName]

    if log:
        print("section Name = %s" % sectionName)
        print("section ID = %s" % sectionId)
    
    First_URL = 'http://m.news.naver.com/section/moreItemList.json?' + "sectionId=%s" % sectionId
    response = requests.get(First_URL)
    result = parse_response(response, log=log)
    
    articleList = result['articles']
    
    if log:
        for article in result['articles']: 
            print("article ID : %s" % article['itemId'])
        
    for i in range(1, limit):
        data = dict()
        data['sectionId'] = sectionId
        data['componentId'] = result['componentId']
        data['itemId'] = result['articles'][-1]['itemId']
        
        # 파일 이름 비교
        
        URL = "http://m.news.naver.com/section/moreItemList.json"
        response = requests.post(URL, data=data)
        result = parse_response(response, log=log)
        
        if log:
            print("index : %s" % i)
            for article in result['articles']: 
                print("Item ID : %s" % article['itemId'])

        #for article in result['articles']:
        #    print(article['itemId'])
        articleList = articleList + result['articles']
        
    return articleList


# In[9]:


# response --> {componentId: int, pageNavigation: int, articles: [article, ...]}
def parse_response(response, log=False):
    
    if response.status_code == 200:
        result = response.json()['message']
        if result["success"]:
            #print(result['contents']['articles'][0].keys())
            result = result['contents']

            if log:
                print()
                print("-- Article log start --")
                print(result['componentId'])
                print(result['pageNavigation'])
                for article in result['articles']:
                    for (k, v) in article.items():
                        print ("- %s : %s" % (k, v))
                    print()
                print("-- Article log end --")
                print()
                
            return result

        else:
            print("Error with Naver request %s" % result["success"])
            return False
    else:
        print("Error with HTTP code %s" % response.status_code)
        return False


# In[10]:


# 메인화면 뉴스묶음 크롤링은 별도로 구현
def request_list(k):
    data = {"page": str(k)}
    navernews_url = "http://m.news.naver.com/mainNews/moreMainNews.json"
    r = requests.post(navernews_url, data=data)
    data = json.loads(r.text)
    #articleList = []
    #for articleData in data['message']['itemList']:
    #    # data의 데이터 선택 및 article 클래스 생성
    #    article = NewsArticle(articleData)
    #    articleList.append(article)
    #return articleList
    return data["message"]['itemList']

def requestMainSection(k):
    l = list()
    for i in range(k):
        l = l + request_list(i)
    return l



# In[11]:


# 데이터베이스 삽입
def section_newsCrawler(sectionName, limit):
    sectionId = section[sectionName]
    tableName = dbName[sectionName]
    l = requestBySection(sectionName, limit=limit, log=False)
    # 시간 역순
    l.reverse()
    for i in l:
        j = NewsArticle(i)
        insert_article(tableName, j.itemId, str(j))
    return

def main_newsCrawler(limit):
    l = requestMainSection(limit)
    l.reverse()
    for i in l:
        j = NewsArticle(i)
        insert_article('article_all', j.itemId, str(j))
    return


# In[ ]:


def crawl(limit):
    processes = []
    
    p = Process(target=main_newsCrawler, args=(limit, ))
    p.start()
    processes.append(p)

    for sectionName in section.keys():
        p = Process(target=section_newsCrawler, args=(sectionName, limit))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


# In[ ]:


start = timer()
crawl(10)
end = timer()
print(end - start)

while True:
    start = timer()
    crawl(10)
    end = timer()
    print(end - start)
    time.sleep(100)


# In[ ]:





# In[ ]:





