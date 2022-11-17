#from bs4 import BeautifulSoup as bs
#from urllib.request import urlopen
import requests
from lxml import etree, html
from requests import get
from requestUrl import *
from productModel import ProductModel

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
    iterator = 0
    for n in node:
        categorie = n.xpath('./li/a')
        if categorie == null:
            Log(f"Não foi possivel coletar os link {n}")
            iterator = iterator + 1
        elif iterator == 10:
            break
        else:
            for c in categorie:
                link = c.attrib["href"]
                Categories.append(link)
                iterator = iterator + 1
                if iterator == 10:
                    break

Log(f"{len(Categories)} categorias coletadas")

#endregion

#region [GetProductFromCategorie]

linkProduct = []

for l in Categories:
    url = f"{_urlPrincipal}{l}"
    categories = RequestUrl(url)
    if categories == None:
        Log("Não foi possivel coletar o categorias")
    else:
        nodes = categories.xpath('//*[@id="title-pdp-link"]')
        for n in nodes:
            if n == None:
                Log(f"Não foi possivel coletar os link {n}")
            else:
                linkProd = n.attrib["href"]
                linkProduct.append(linkProd)
                #Log(f"Link coletado {linkProd}")

#print(len(linkProduct))

#endregion

#region [GetProduct]

product = []

productModel = ProductModel

for p in linkProduct:
    urlProduct = f"{_urlPrincipal}{p}"
    products = RequestUrl(urlProduct)
    if products == None:
        Log(f"Não foi possivel coletar produto {urlProduct}")
    
    else:
        nome = products.xpath('//*[@id="__next"]/div[1]/div/div[4]/div[2]/div[1]/div[1]/h1')
        for n in nome:
            productModel.ProductName = n.text

        ean = products.xpath('//*[@id="__next"]/div[1]/div/div[4]/div[2]/div[1]/div[1]/div[1]/div[2]/text()[3]')
        for e in ean:
            productModel.ProdcutEan = e
#endregion