from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
from lxml import etree, html
from requests import get
from requestUrl import *
from productModel import ProductModel

#region [Properties]

'''
Esses links são usados para fazer as requisições no site da empresa desejada.
Esse crawler foi construido para fazer paginação, então ele acessa a _URL1 e depois busca dentro da pagina as urls de categorias
_URL1 -> É da pagina principal do site
_URL2 -> É uma url de busca, quando adicionamos um nome no final dela somos direcionados a todos os produtos relacionados
'''
_URL1 = "https://www.sodimac.com.br"

_URL2 = "https://www.sodimac.com.br/sodimac-br/category/cat170440/telhas/?sTerm="

#endregion

#region [Search]

#Lista pra armazenar todos os links coletados na requisição
Categories = []

#Chamada da url principal
site = RequestUrl(_URL1)

#Coletando link na pagina por meio de indicador "xpath", que indica para o crawler qual intem deve ser coletado dentro do siet
node = site.xpath('//ul[@class="MenuMobile-module_limited__xa3jW"]/li/div/div/ul/li/div/ul')
#Verificando caso o intem seja nulo ou vazio
if node == None or len(node) == 0:
    Log("Não foi possivel coletar o categorias")
#Se não for nulo ele coleta o link da categoria 
else:
    iterator = 0
    for n in node:
        #node retorna uma lista então vamos iterar dentro dela usando "for"  buscando dentro de cada item da lista o link que queremos
        #Na linha abaixo usamos o apontador "xpath" para localizar a tag que tem o link da categoria 
        categorie = n.xpath('./li/a')
        #Verifica se categorie não esta vazia ou nula
        if categorie == None or len(categorie) == 0:
            Log(f"Não foi possivel coletar os link {n}")
        #Aqui eu limito a coleta do links para 10, ai ele para a coleta das categorias
        elif iterator == 10:
            break
        else:
            for c in categorie:
                #Aqui ele coleta o link e salva dentro da lista global "Categories"
                link = c.attrib["href"]
                #Interpolação do link principal com o coletado nas categorias
                Categories.append(f"{_URL1}{link}")
                iterator = iterator + 1
                
#Mostra quantos links foram coletados 
Log(f"{len(Categories)} categorias coletadas")

#endregion

#region [GetProductFromCategorie]

#Lista pra armazenar todos os links dos produtos das categorias
linkProduct = []

iterator = 0
for l in Categories:
    url = l
    #Chamada da url principal
    categories = RequestUrl(url)
    if categories == None or len(categories) == 0:
        Log("Não foi possivel coletar o categorias")
    
    else:
        #Coletando link na pagina por meio de indicador "xpath", que indica para o crawler qual intem deve ser coletado dentro do siet
        nodes = categories.xpath('//*[@id="title-pdp-link"]')
        for n in nodes:
            if n == None or len(nodes) == 0:
                Log(f"Não foi possivel coletar os link {n}")
            elif iterator == 30:
                break
            else:
                #Na linha abaixo estamos coletando os links dos produtos contidos no atributo href dentro da tag 
                linkProd = n.attrib["href"]
                #Interpolação do link principal com o coletado nas categorias
                linkProduct.append(f"{_URL1}{linkProd}")
                iterator = iterator + 1
                
                #Log(f"Link coletado {linkProd}")

#Mostra quantos links foram coletados 
Log(f"links coletados: {len(linkProduct)}")

#endregion

#region [GetProduct]

#Lista pra armazenar todos os links dos produtos das categorias
product = []

#Estanciando o modelo de produto para depois ser adicionado na lista "product"
productModel = ProductModel

for p in linkProduct:
    #Aqui estamos iterando dentro da nosta lista para poder fazer a requisição dentro de link dentro da lista "linkProduct"
    products = RequestUrl(p)
    #Verificando se não é nulo ou vazio
    if products == None or products == 0:
        Log(f"Não foi possivel coletar produto {p}")
    
    else:
        #Buscando o nome do produto
        nome = products.xpath('//*[@id="__next"]/div[1]/div/div[4]/div[2]/div[1]/div[1]/h1')
        for n in nome:
            #Adicionando o nome dentro do nosso modelo criado previamente 
            productModel.ProductName = n.text

        #Coletando ean
        ean = products.xpath('//*[@id="__next"]/div[1]/div/div[4]/div[2]/div[1]/div[1]/div[1]/div[2]/text()[3]')
        for e in ean:
            productModel.ProdcutEan = e

        #Coletando preço do produto, que na página esta divida em duas tags diferentes
        priceInt = products.xpath('//*[@id="__next"]/div[1]/div/div[4]/div[2]/div[1]/div[2]/div/div/span[2]')
        priceCoin = products.xpath('//*[@id="__next"]/div[1]/div/div[4]/div[2]/div[1]/div[2]/div/div/span[3]')
        for pi in priceInt:
            price1 = pi.text
        for pc in priceCoin:
            price2 = pc.text
        #Fazendo a interpolação dos preço para armazenar no modelo do produto
        productModel.ProductPrice = f"{price1}{price2}"
        #Colocando qual a meoda 
        productModel.Currency = "R$"
        #Colocando o vendedor
        productModel.ProductSeller = "Sodimac"
        
        #Coletando a descrição do produto
        description = products.xpath('//*[@id="description"]/div[1]/p[1]')
        if description == None or len(description) == 0:
            Log(f"Não existe descrição {p}")
        else:
            for t in description:
                productModel.Description = t.text

    product.append(productModel)
    Log("Product collected")

print(len(product))

#endregion