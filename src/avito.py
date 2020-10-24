#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse as up
from fake_useragent import UserAgent
import csv
import random
#from socket import socket
#from socks import socksocket
#import stem
#from stem import Signal
import numpy as np
import re
from googletrans import Translator
from time import sleep


translator = Translator()
def translate(word):
    translation = translator.translate(word).text
    if translation == 'the black':
        return 'BLACK'
    else:
        return translation.upper()

protip_translator = {
    'бензин': 'GASOLINE',
    'дизель': 'DIESEL',
    'гибрид': 'HYBRID',
    'электро': 'ELECTRO',
    'полный': 'ALL_WHEEL_DRIVE',
    'передний': 'FORWARD_CONTROL', 
    'задний': 'BACKWARD_CONTROL',
    'седан': 'SEDAN',
    'внедорожник': 'ALLROAD',
    'хетчбэк': 'HATCHBACK',
    'купе': 'COUPE',
    'универсал': 'WAGON',
    'левый': 'LEFT',
    'правый': 'RIGHT',
    'битый': 'BEATEN',
    'не битый': 'NOT_BEATEN',
    'робот': 'AMT',
    'автомат': 'AT',
    'вариатор': 'CVT',
    'механика': 'MT'
}     

def write_csv(data):
    with open('avito_moscow_audi_new_try.csv', 'a', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['brand'],
                         data['model'],
                         data['year'],
                         data['price'],
                         data['mileage'],
                         data['horsepower'],                         
                         data['engine_capacity'],
                         data['engine_type'],
                         data['gear'],
                         data['transmission'],
                         data['bodywork'],
                         data['doors_num'],
                         data['steering_wheel'],
                         data['tech_condition'],
                         data['owners_num'],
                         data['vin'],                         
                         data['color']))
        
def build_link_by_user_params(city : str, brand : str):
    
    return f'https://www.avito.ru/{city}/avtomobili/{brand}-ASgBAgICAUTgtg3elyg?'


def get_soup_for_page_links(page : int, city : str, brand : str):
    
    params = {'cd' : 1,
              'radius' : 200}
    if page and page > 1:
        params['p'] = page
    
    session = requests.Session()
    url = build_link_by_user_params(city, brand)
    #session.cookies.clear()
    response = session.get(url, 
                            params = params, 
                            headers = {
                                'User-Agent' : UserAgent().chrome, 
                                'Acept-Language' : 'ru'
                            })
    if not response.ok:
        return []
    
    soup_with_links = bs(response.content, 'lxml')
    return soup_with_links
    
def get_page_links(page : int, city : str, brand : str):
      
    card_links = get_soup_for_page_links(page, city, brand).find_all(lambda tag: tag.name == 'a' 
                                                        and tag.get('class') == ['snippet-link'])
    card_links = ['https://www.avito.ru' + link.attrs['href'] 
                      for link in card_links 
                      if (city in link.attrs['href'].split('/') 
                          and 'glb_klass' not in link.attrs['href'].split('/'))]  
    return card_links 

def get_maxnum_page_possible_to_parse(page : int, city : str, brand : str):
    pagination = get_soup_for_page_links(page, city, brand).select('span.pagination-item-1WyVp')
    return int([page.text for page in pagination][-2])

def get_soup_for_offer_page(link : str):

    session = requests.Session()
    #session.cookies.clear()
    response = session.get(link, headers = {
                                'User-Agent' : UserAgent().chrome, 
                                'Acept-Language' : 'ru'
                            }
                          )

    soup_with_offer = bs(response.content, 'lxml')
    return soup_with_offer

def get_car_data(link : str):
    
    car_with_all_chars = {}
    char_set = {}
    soup_with_offer = get_soup_for_offer_page(link)
    char_list_value = soup_with_offer.select('li.item-params-list-item')
    for char_value in char_list_value:
        names_values = char_value.get_text().split(':')
        char_set[names_values[0].strip()] = names_values[1].strip()  
    
    if char_set.get('Марка'):
        
        try:
            price = soup_with_offer.find('span',{'itemprop':'price'})['content']
        except:
            price = None
        
        try:
            horsepower = re.compile('([0-9]* л.с.)').findall(str(char_set.get('Модификация','')))[0].replace(' л.с.','')
        except:
            horsepower = None
            
        try:
            engine_capacity = re.compile('[0-9][.][0-9]').findall(str(char_set.get('Модификация','')))[0]
        except:
            engine_capacity = None            
 
        
        data = {'brand' : char_set.get('Марка',''),
               'model' : char_set.get('Модель',''),
               'year' : char_set.get('Год выпуска',''),
               'price' : int(price) if price else '',
               'mileage' : int(str(char_set.get('Пробег',0)).replace('\xa0км','')),
               'horsepower' : int(horsepower) if horsepower else '', 
               'engine_capacity' : float(engine_capacity) if engine_capacity else '',                
               'engine_type' : char_set.get('Тип двигателя',''),
               'gear' :  char_set.get('Коробка передач',''),
               'transmission' : char_set.get('Привод',''),
               'bodywork' : char_set.get('Тип кузова',''),
               'doors_num' : char_set.get('Количество дверей',''),
               'steering_wheel' : char_set.get('Руль',''),
               'tech_condition' : char_set.get('Состояние',''),
               'owners_num' : int(str(char_set.get('Владельцев по ПТС',0)).replace('+','')), 
               'vin' : char_set.get('VIN или номер кузова',''),
               'color' : translate(char_set.get('Цвет',''))
                }

        return data

def rename_features_for_merge(link : str):
  
  """Get raw data and unify for the next merge with res from other parsers"""
    
    raw_data = get_car_data(link)
    unified_data = {key: protip_translator.get(val, val) 
                    for key, val in raw_data.items()}
    write_csv(unified_data)

def get_all_cards_info_from_current_page(page : int, city : str, brand : str):
    
    links_list = get_page_links(page, city, brand)
    for link in links_list:
        get_car_data(link)
        sleep(random.randint(2,7))

def parse_pages_as_example(page: int, city : str, brand : str):
    
    for pag in range(1,page):
        get_all_cards_info_from_current_page(pag, city, brand)
        sleep(random.randint(2,7))

def parse_all_pages(city : str, brand : str):
    
    for page in get_maxnum_page_possible_to_parse(page = 1):
        get_all_cards_info_from_current_page(page)
        sleep(random.randint(2,7))
        
if __name__ == '__main__':
    parse_pages_as_example(2,'moskva','audi')

