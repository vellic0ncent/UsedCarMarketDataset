from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import csv
import pandas as pd
import re


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://auto.youla.ru/moskva/cars/used/audi/?page="  

def url_adress(current_page):
    next_page = url + current_page + "#serp"
    return next_page
    
def write_to_csv(data):
    with open('youla_AUDI_2.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['brand'],
                         data['model'],
                         data['price'],
                         data['Год выпуска'],
                         data.get('mileage', None),
                         data['engine_type'],
                         data['Привод'],
                         data['Цвет'],
                         data['bodywork'],
                         data['doors_num'],
                         data.get('Руль', None),
                         data.get('VIN', None),
                         data.get('Владельцев', None),
                         data['horsepower'],
                         data['engine_capacity']))
                         
def read_data_auto(aut):
    for item in aut:
        auto_name = item.find('a', {'class': 'SerpSnippet_name__3F7Yu SerpSnippet_titleText__1Ex8A blackLink'}).text
        brand, model = auto_name[:5], auto_name[5:]
        link = item.find('a', {'data-target': 'serp-snippet-title'}).get('href')
        html = urlopen(link, context=ctx).read()
        soup_detailed = BeautifulSoup(html, "html.parser")
        card_names = soup_detailed.select('div.AdvertSpecs_label__2JHnS') 
        card_char = soup_detailed.select('div.AdvertSpecs_data__xK2Qx') 
        dict_value ={}
        for name, char in zip(card_names, card_char):
            name_in_card,char_in_card = name.get_text(),char.get_text()
            dict_value[name_in_card] = char_in_card
        dict_value['mileage'] = int(dict_value['Пробег'].split('км')[0].replace(' ','')) 
        dict_value['engine_type'] = dict_value['Двигатель'].split('/')[0] 
        dict_value['engine_capacity'] = dict_value['Двигатель'].split('/')[1]
        dict_value['bodywork'] = dict_value['Кузов'].split(' ')[0]
        dict_value['doors_num'] = str(re.findall('\d', dict_value['Кузов']))
        data = {'brand': brand, 
               'model': model}
        
        data_all = {**data, **dict_value}
        write_to_csv(data_all)  
        
#считываем первую страницу, идёт без номера
def data_for_first_page():
    global url
    atpos = url.find('?')
    url = url[:atpos]
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    res = soup.find('div', {"id": "serp"})
    aut = res.find_all('article', {'class': 'SerpSnippet_snippet__3O1t2 app_roundedBlockWithShadow__1rh6w'})      
    read_data_auto(aut)             
    
# остальные страницы
def data_for_more_pages(current_page):
    url = url_adress(current_page)
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    res = soup.find('div', {"id": "serp"})
    aut = res.find_all('article', {'class': 'SerpSnippet_snippet__3O1t2 app_roundedBlockWithShadow__1rh6w'})    
    read_data_auto(aut)

#записываем заголовки, первую страницу, остальные страницы
with open('yula_AUDI.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(names)
data_for_first_page()    
for i in range(2,14): #(2,14):
    data_for_more_pages(str(i))  
