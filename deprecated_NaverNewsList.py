from bs4 import BeautifulSoup as BS
import urllib.request

MAIN_URL = 'http://m.news.naver.com/'

def get_articles():
    soup = BS(urllib.request.urlopen(MAIN_URL),
            'html.parser',
            from_encoding = 'utf-8');
    for i in (soup.find_all('div', class_ = 'r_group _reset')):
        print(i);

get_articles();
