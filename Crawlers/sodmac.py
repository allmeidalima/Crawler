#from bs4 import BeautifulSoup as bs
#from urllib.request import urlopen
from requests import get
import requests
from Functions.requestUrl import RequestUrl
from lxml import etree, html

#region [Properties]

_urlPrincipal = "https://www.sodimac.com.br/"
_urlBusca = "https://www.sodimac.com.br/sodimac-br/category/cat170440/telhas/?sTerm="

#endregion

#region [Search]

links = []

htmll = RequestUrl(_urlPrincipal)

node = htmll.xpath('//ul[@class="MenuMobile-module_limited__xa3jW"]/li/div/div/ul/li/div/ul')
if node != " ":
    for n in node:
        categorie = n.xpath('./li/a')
        if categorie != " ":
            for c in categorie:
                link = c.attrib["href"]
                links.append(link)

print(links)

#endregion