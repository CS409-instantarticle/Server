from bs4 import BeautifulSoup as BS
import urllib.request

def get_text(URL):
    source_code_from_URL = urllib.request.urlopen(URL);
    soup = BS(source_code_from_URL, 'html.parser', from_encoding = 'utf-8');
    return soup.find_all('div', id='dic_area')