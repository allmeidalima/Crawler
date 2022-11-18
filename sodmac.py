from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
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
        elif iterator == 10:
            break
        else:
            for c in categorie:
                link = c.attrib["href"]
                Categories.append(link)
                iterator = iterator + 1
                

Log(f"{len(Categories)} categorias coletadas")

#endregion

#region [GetProductFromCategorie]

linkProduct = []

iterator = 0
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
            elif iterator == 50:
                break
            else:
                linkProd = n.attrib["href"]
                linkProduct.append(linkProd)
                iterator = iterator + 1
                
                #Log(f"Link coletado {linkProd}")

print(len(linkProduct))

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

        priceInt = products.xpath('//*[@id="__next"]/div[1]/div/div[4]/div[2]/div[1]/div[2]/div/div/span[2]')
        priceCoin = products.xpath('//*[@id="__next"]/div[1]/div/div[4]/div[2]/div[1]/div[2]/div/div/span[3]')
        for pi in priceInt:
            price1 = pi.text
        for pc in priceCoin:
            price2 = pc.text
        productModel.ProductPrice = f"{price1}{price2}"
        productModel.Currency = "R$"
        productModel.ProductSeller = "Sodimac"

        description = products.xpath('//*[@id="description"]/div[1]/p[1]')
        if description == None:
            Log("Não existe descrição")
        else:
            for t in description:
                productModel.Description = t.text

    product.append(productModel)
    Log("Product collected")

print(len(product))

#endregion