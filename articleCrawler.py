from bs4 import BeautifulSoup as BS
import urllib.request

def get_text(URL):
    source_code_from_URL = urllib.request.urlopen(URL);
    soup = BS(source_code_from_URL, 'html.parser', from_encoding = 'utf-8');
    print(soup.find_all('div', id="dic_area"))

#print(get_text("http://m.news.naver.com/read.nhn?oid=079&aid=0002964148"))
get_text("http://m.news.naver.com/read.nhn?oid=079&aid=0002964148")