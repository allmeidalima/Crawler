#from bs4 import BeautifulSoup as bs
#from urllib.request import urlopen
import requests
from lxml import etree, html
from requests import get
from requestUrl import *

#region [Properties]

_urlPrincipal = "https://www.sodimac.com.br"

_urlBusca = "https://www.sodimac.com.br/sodimac-br/category/cat170440/telhas/?sTerm="

#endregion

#region [Search]

Categories = []

site = RequestUrl(_urlPrincipal)

node = site.xpath('//ul[@class="MenuMobile-module_limited__xa3jW"]/li/div/div/ul/li/div/ul')
if node == null:
    Log("Não foi possivel coletar o categorias")
else:
    for n in node:
        categorie = n.xpath('./li/a')
        if categorie == null:
            Log(f"Não foi possivel coletar os link {n}")
        else:
            for c in categorie:
                link = c.attrib["href"]
                Categories.append(link)

#print(Categories)

#endregion

#region [GetProductFromCategorie]

for l in Categories:
    url = f"{_urlPrincipal}{l}"
    categories = RequestUrl(url)
    nodes = categories.xpath('//*[@id="__next"]/div[1]/div/div[5]/div[3]/div/div[1]/div[3]/div[1]/div/div[3]')
    if nodes == 0:
        Log("Não foi possivel coletar o categorias")
    else:
        for n in nodes:
            categorie = n.xpath('./a')
            if categorie == None:
                Log(f"Não foi possivel coletar os link {n}")
            else:
                for c in categorie:
                    link = c.attrib["href"]
                    Categories.append(link)


#endregion