from bs4 import BeautifulSoup as BS
import urllib.request

def remove_tag(text, tag):
    while text.find("<" + tag) != -1:
        start_index = text.find("<" + tag)
        end_index = start_index
        while text[end_index] != '>':
            end_index += 1
        text = text[:start_index] + text[end_index+1:]
    return text

def get_text(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BS(source_code_from_URL, 'html.parser', from_encoding = 'utf-8')
    result = soup.find_all('div', id="dic_area")[0]
    return(remove_tag(remove_tag(str(result).replace("</br>","").replace("<br>","\n").replace("</tr>","").replace("</td>","").replace("<tr>","").replace("<td>","").replace("<strong>","").replace("</strong>","").replace("<b>","").replace("</b>","").replace("<center>","").replace("</center>",""),"font"),"/font"))