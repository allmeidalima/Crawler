from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from requests import get
from lxml import etree, html
#import json

    
def RequestUrl(site):
    responseUrl = get(site)
    elementHtml = html.fromstring(responseUrl.text)
    return elementHtml

def RequestUrlBs4(site):
    responseUrlBs4 = get(site)
    elementHtmlBs4 = bs(responseUrlBs4.text, "html.parser")
    return elementHtmlBs4


def Log(string):
    log = print(string)
    return log

def null():
    return null 
