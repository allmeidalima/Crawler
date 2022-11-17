#from bs4 import BeautifulSoup as bs
#from urllib.request import urlopen
from requests import get
from lxml import etree, html
#import json


def RequestUrl(site):
    responseUrl = get(site)
    elementHtml = html.fromstring(responseUrl.text)
    return elementHtml
