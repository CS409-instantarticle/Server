
# coding: utf-8

# In[1]:


from flask import Flask, request, session, g, redirect, url_for,      abort, render_template, flash
import sqlite3
import pickle 

max_items = 12

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
    '전체' : "article_all",
    '정치' : "article_politics",
    '경제' : "article_economy",
    '사회' : "article_society",
    'IT'   : "article_it",
    '생활' : "article_life",
    '세계' : "article_world"
}

section_etok= {
    'Home' : '홈',
    'Politics' : '정치',
    'Economy' : '경제',
    'Society' : '사회',
    'Life' : '생활',
    'World' : '세계'
}


# In[2]:


conn_all = sqlite3.connect("article_all.db")
conn_politics = sqlite3.connect("article_politics.db")
conn_economy = sqlite3.connect("article_economy.db")
conn_society = sqlite3.connect("article_society.db")
conn_it = sqlite3.connect("article_it.db")
conn_life = sqlite3.connect("article_life.db")
conn_world = sqlite3.connect("article_world.db")

c_all = conn_all.cursor()
c_politics = conn_politics.cursor()
c_economy = conn_economy.cursor()
c_society = conn_society.cursor()
c_it = conn_it.cursor()
c_life = conn_life.cursor()
c_world = conn_world.cursor()

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


# In[3]:


def select_article(tablename, index, limit):
    cur = c[tablename]
    cur.execute("select idx, itemid, json from %s where idx <= %s order by idx desc limit %s " % (tablename, index, limit))
    return [(row[0], row[1], pickle.loads(row[2])) for row in cur]



# In[ ]:


app = Flask(__name__)


# 베이스 디렉토리
@app.route('/')
def index():
    return "Hello, world!"


@app.route("/Article/<index>")
def article(index):
    select_article(dbName[section], index, 1)
    return str(s)



@app.route("/ArticleList/<index>")
def articleList(index):
    index = int(index)
    li = select_article('article_all', index, max_items)
    res = list()
    for i in li:
        s = eval(i[2])
        s['ArticleMainIndex'] = i[0]
        res.append(s)
    return str(res)



@app.route("/ArticleSection/<section>/<index>")
def articleSection(section, index):
    if section in section_etok.keys() : 
        section = section_etok[section]
    
    if section == "홈":
        section = "전체"
    
        
    li = select_article(dbName[section], index, max_items)
    res = list()
    for i in li:
        s = eval(i[2])
        s['ArticleMainIndex'] = i[0]
        res.append(s)
    return str(res)
    


# In[ ]:


app.run("kaist.tk", port=1234)


# In[ ]:





# In[ ]:





