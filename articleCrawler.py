from bs4 import BeautifulSoup as BS
import urllib.request

def get_text(URL):
    source_code_from_URL = urllib.request.urlopen(URL);
    soup = BS(source_code_from_URL, 'html.parser', from_encoding = 'utf-8');
    return soup.find_all('div', id='dic_area')

#print(get_text("http://m.news.naver.com/read.nhn?oid=421&aid=0002706598"))
#print(get_text("http://m.news.naver.com/read.nhn?oid=052&aid=0001004863&sid1=103&mode=LSD"))
print(get_text("http://m.news.naver.com/read.nhn?oid=469&aid=0000200834"))
