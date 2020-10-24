from urllib.request import urlopen
from bs4 import BeautifulSoup
from googletrans import Translator
import ssl
import csv
import re


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://auto.youla.ru/moskva/cars/used/audi/?page="  
names = ['brand', 'model', 'year', 'price', 'mileage', 'horsepower', 'engine_capacity', 'engine_type', 'gear', 'transmission', 'bodywork', 'steering_wheel', 'tech_condition', 'owners_num', 'doors_num', 'VIN', 'color']
    
def url_adress(current_page):
    next_page = url + current_page + "#serp"
    return next_page
    
def write_to_csv(data):
    with open('youla.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['brand'],
                         data['model'],
                         data['Год выпуска'],
                         data['price'],
                         data.get('mileage', None),
                         data.get('horsepower', None),
                         data['engine_capacity'],
                         data['engine_type'],
                         data['gear'],
                         data['transmission'],
                         data['bodywork'],
                         data.get('steering_wheel', None),
                         ' ',
                         data.get('Владельцев', None),
                         data['doors_num'],
                         data.get('VIN', None),
                         data['color']))
                         
engine_type_enum = {
            'Дизель ': 'DIESEL',
            'Бензин ': 'GASOLINE'
}       

gear_enum = {
            'Полный': 'ALL_WHEEL_DRIVE',
            'Полный подключаемый': 'ALL_WHEEL_DRIVE',  
            'Передний': 'FORWARD_CONTROL',
            'Задний': 'BACKWARD_CONTROL'
}                         

transmission_enum = {
            'Автомат': 'AT',
            'Робот': 'AMT',  
            'Вариатор': 'CVT',
            'Механика': 'MT'
}

bodywork_enum= {
            'Седан': 'SEDAN',
            'Кроссовер': 'ALLROAD',  
            'Хетчбэк': 'HATCHBACK',
            'Купе': 'COUPE',
            'Универсал': 'WAGON',
            'Кабриолет': 'CABRIO'
}


translator = Translator()

def translate(word):
    return translator.translate(word).text
    
def replace_to_enum(value, enum_mappings):
    if value is not None:
        return enum_mappings[value]
    else:
        return None
                         
def read_data_auto(aut):
    for item in aut:
        auto_name = item.find('a', {'class': 'SerpSnippet_name__3F7Yu SerpSnippet_titleText__1Ex8A blackLink'}).text
        brand, model = auto_name[:4], auto_name[5:].split(',')[0]
        price = item.find('div', {'data-target': 'serp-snippet-price'}).text
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
        dict_value['engine_type'] = replace_to_enum(dict_value['Двигатель'].split('/')[0], engine_type_enum) 
        dict_value['gear'] = replace_to_enum(dict_value['Привод'], gear_enum)
        dict_value['transmission'] = replace_to_enum(dict_value['КПП'], transmission_enum)
        dict_value['engine_capacity'] = dict_value['Двигатель'].split('/')[1]
        dict_value['engine_capacity'] = dict_value['engine_capacity'].split('л')[0]  #.split(' ')[0]
        dict_value['bodywork'] = replace_to_enum(dict_value['Кузов'].split(' ')[0], bodywork_enum)
        dict_value['doors_num'] = ''.join(re.findall('\d', dict_value['Кузов'])) 
        dict_value['horsepower'] = dict_value['Мощность'].split(' л. с.')[0]
        dict_value['color'] = translate(dict_value['Цвет'])
        if dict_value.get('Руль', None) == 'Левый':
            dict_value['steering_wheel'] = "LEFT"
        elif dict_value.get('Руль', None) == 'Правый':
            dict_value['steering_wheel'] = "RIGHT"
        data = {'brand': brand, 
               'model': model,
               'price': price}
               
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
with open('youla.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(names)
data_for_first_page()    
for i in range(2,11): #(2,14):
    data_for_more_pages(str(i))  
