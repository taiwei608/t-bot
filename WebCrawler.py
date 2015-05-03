import requests
from bs4 import BeautifulSoup
import chardet
import re

headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0' }
cookies = { 'over18' : '1' }

def get(URL):
    try:
        if 'ptt.cc' in URL:
            r = requests.get(URL, allow_redirects=True, timeout=6, headers=headers, cookies=cookies)
        else:
            r = requests.get(URL, allow_redirects=True, timeout=6, headers=headers)
    except requests.ConnectionError:
        return "page connection error"
    except:
        return "page timeout"

    if r.status_code != 200:
        return "page not found"

    charset = chardet.detect(r.content).get('encoding')
    if charset == 'Big5':
        r.encoding = 'big5'
    else:
        r.encoding = 'utf-8'
    try:
        content_type =  r.headers['content-type']
    except:
        content_type = ''

    print "content_type = " + content_type
    print "r.text = " + r.text

    m = re.match(r'image/[png|jpeg|jpg|gif]', content_type, re.I)
    if m:
        return "Link is a picture"
    else:
        soup = BeautifulSoup(r.text)
        """ Extract Page title """
        #print soup
        if r.encoding == 'big5':
            return "[Title] " + soup.title.string.encode('utf-8')
        else:
            return "[Title] " + soup.title.string
