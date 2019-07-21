import requests
import pandas
import json
import re
import os
import urllib.request as request
from bs4 import BeautifulSoup

folder = os.getcwd()

print("Copiar textualmente una de las opciones escritas en los parentesis")

prop = input("Especificar tipo de propiedad deseada (Departamentos, Casa, o PH): ")
operation = input("Nombrar tipo de operacion a realizar (Alquiler o Comprar): ")
zone = input("Nombrar barrio de la propiedad buscada: ").replace(" ","-").replace("ñ","n")

if operation == "comprar":
    maxBudget = input("Presupuesto maximo en USD: ")
    minBudget = input("Presupuesto minimo en USD: ")
    currency = "dolar"
    operation = "venta"
else:
    maxBudget = input("Presupuesto maximo: ")
    minBudget = input("Presupuesto minimo: ")
    currency = "pesos"

amb = input("Cantidad de ambientes en forma numerica: ")

#https://stackoverflow.com/questions/3411771/multiple-character-replace-with-python
#https://www.zonaprop.com.ar/departamentos-alquiler-belgrano-2-ambientes-15000-22000-pesos-pagina-2.html
zonaPropUrl = ("https://www.zonaprop.com.ar/" + str.lower(prop) + "-" + str.lower(operation) + "-" + str.lower(zone) + "-" + (amb) + "-ambientes-" + (minBudget) + "-" + (maxBudget)+ "-" + str.lower(currency) + ".html")
print(zonaPropUrl)
print(" ")

source = requests.get(zonaPropUrl)
content = source.content

soup = BeautifulSoup(content, "html.parser")

propertyQuantity = soup.find("h1", {"class":"list-result-title"}).find("b", recursive = False).text
print((propertyQuantity) + " propiedades.")
pageCalculation = (int(propertyQuantity)/20)
pageQuantity = (round(pageCalculation))
print(pageQuantity)


all = soup.find_all("div", {"class":"general-content"})

l = []
base_url = ("https://www.zonaprop.com.ar/" + str.lower(prop) + "-" + str.lower(operation) + "-" + str.lower(zone) + "-" + (amb) + "-ambientes-" + (minBudget) + "-" + (maxBudget)+ "-" + str.lower(currency))
for page in range(1, pageQuantity, 1):
    pageQuantity = (str(pageQuantity))
    finalUrl = base_url + "-pagina-" + str(page) + ".html"
    print(finalUrl)
    source = requests.get(finalUrl)
    content = source.content
    soup = BeautifulSoup(content, "html.parser")
    all = soup.find_all("div", {"class":"general-content"})
   # print(soup.prettify())
    for item in all:
        dictionary = {}
        ### ZONAPROP ###
        address = item.find("span", {"class":"posting-location go-to-posting"}).text.lstrip()
        addressFixed = re.sub('\s+', ' ', address).strip()
        #https://stackoverflow.com/a/2077906/5150543
        print(addressFixed)
        dictionary["Address"] = addressFixed
        try:
            price = item.find("span", {"class":"first-price"}).text.lstrip()
            print(price)
            dictionary["Price"] = price
        except:
            pass
        try:
            expenses = item.find("span", {"class":"expenses"}).text.lstrip()
            print(expenses) 
            dictionary["Expenses"] = expenses
        except:
            dictionary["Expenses"] = "Sin expensas."
            pass
        specs = item.find("ul", {"class":"main-features go-to-posting"}).text.lstrip().replace("\n"," |")
        print(specs)
        dictionary["Specs"] = specs
        publicationDate = item.find("ul", {"class":"posting-features go-to-posting"}).text.lstrip().replace("\n"," | ")
        print(publicationDate)
        dictionary["Publication Date"] = publicationDate
        l.append(dictionary)
        image = item.find("div", {"class":"slide-content go-to-posting is-selected"})

save = input("Guardar resultados en la base de datos? si/no: ")
if save == "si":
    dataframe = pandas.DataFrame(l)
    dataframe.to_json("dataframe.json")
else:
    pass                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
