import requests
from bs4 import BeautifulSoup
import csv
from googletrans import Translator

URL = "https://irr.ru/cars/passenger/audi/"

names = ['brand', 'model', 'year', 'price', 'mileage', 'horsepower', 'engine_capacity', 'engine_type', 'gear', 'transmission', 'bodywork', 'steering_wheel', 'tech_condition', 'owners_num', 'doors_num', 'VIN', 'color']

def get_html (url, params=None):
    r = requests.get(url, params)
    r.encoding = 'utf-8'
    return  r

translator = Translator()
def translate(word):
    return translator.translate(word).text


def get_pages(url):
    try:
        html=get_html(URL)
        soup = BeautifulSoup (html.text, 'html.parser')
        items = soup.find_all('a', class_='pagination__pagesLink')
        return (int(items[-1].text))
    except IndexError:
        return 1

def write_to_csv(data):
    with open('irr.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((data['brand'],
                         data['model'],
                         data['year'],
                         data['price'],
                         data['mileage'],
                         data['horsepower'],
                         data['engine_capicity'],
                         data['engine_type'],
                         data['gear'],
                         data['transmission'],
                         data['bodywork'],
                         data['steering_wheel'],
                         data['tech_condition'],
                         data['owners_num'],
                         data['doors_num'],
                         data['vin'],
                         data['color'],))

def get_link_list_with_cards(url):
    html=get_html(url)
    link_list = []
    soup = BeautifulSoup (html.text, 'html.parser')
    items = soup.select('.listing__itemTitleWrapper')
    for item in items:
        link=item.find('a')
        link_list.append(link['href'])
    return link_list

def replace_to_enum(value, enum_mappings):

    if value is not None:
        return enum_mappings[value]
    else:
        return None

def get_characteristics_with_page_to_CSV(link_list):

    for link in link_list:
        card = get_html(link)
        card_soup = BeautifulSoup (card.text, 'html.parser')
        characteristics=['Марка','Модель','Год выпуска','Пробег','Тип двигателя','Тип трансмиссии','Тип кузова','Кол-во дверей','Руль','VIN','Кол-во владельцев','Состояние автомобиля','Мощность двигателя','Объем двигателя','Цвет','Привод']
        car={'brand':None,'model':None,'year':None,'mileage':None,'engine_type':None,'transmission':None,'bodywork':None,'doors_num':None,'steering_wheel':None,'vin':None,'owners_num':None,'tech_condition':None,'horsepower':None,'engine_capicity':None,'color':None, 'gear': None}


        try:
            car['color']=(translate(card_soup.find('li',class_='productPage__productColor').get_text())).upper()
            if car['color']=='THE BLACK':
                car['color']='BLACK'

        except AttributeError:
            car['color']=None

        price = card_soup.find('div',itemprop='offers').text
        car['price']=int((price.replace(' руб.', '')).replace('\xa0', ''))

        characteristics_list=card_soup.find_all('li', class_='productPage__infoColumnBlockText')
        for characteristic in characteristics_list:

            characteristic=characteristic.text.split(': ')

            if characteristic[0] in characteristics:


                if characteristic[0]=='Марка':
                    car['brand']=characteristic[1]


                if characteristic[0]=='Модель':
                    car['model']=str(characteristic[1])



                if characteristic[0]=='Год выпуска':
                    car['year']=int(characteristic[1].replace(' г.', ''))


                if characteristic[0]=='Пробег':
                    car['mileage']=int((characteristic[1].replace(' км', '')).replace(', миль', ''))


                if characteristic[0]=='Тип двигателя':
                    car['engine_type']=replace_to_enum(characteristic[1], engine_type_enum)


                if characteristic[0]=='Тип трансмиссии':
                    car['transmission']=replace_to_enum(characteristic[1], transmission_enum)


                if characteristic[0]=='Тип кузова':
                    car['bodywork']=replace_to_enum(characteristic[1], bodywork_enum)


                if characteristic[0]=='Кол-во дверей':
                    car['doors_num']=int(characteristic[1])


                if characteristic[0]=='Руль':
                    car['steering_wheel']=replace_to_enum(characteristic[1], wheel_enum)


                if characteristic[0]=='VIN':
                    car['vin']=characteristic[1]


                if characteristic[0]=='Кол-во владельцев':
                    car['owners_num']=int(characteristic[1])


                if characteristic[0]=='Состояние автомобиля':
                    car['tech_condition']=replace_to_enum(characteristic[1], tech_condition_enum)


                if characteristic[0]=='Мощность двигателя':
                    car['horsepower']=int(characteristic[1].replace(' л.с.', ''))


                if characteristic[0]=='Объем двигателя':
                    car['engine_capicity']=float(characteristic[1].replace(' л', ''))


                if characteristic[0] == 'Привод':
                    car['gear'] = replace_to_enum(characteristic[1], gear_enum)


        if car['model'] is None:
            continue

        write_to_csv(car)

engine_type_enum = {
            'дизель ': 'DIESEL',
            'бензин ': 'GASOLINE'
}

transmission_enum = {
    'автомат ':'at',
    'механика ':'mt',
    'вариатор ':'cvt',
    'робот ':'amt'
}

wheel_enum = {
    'левый ' :  'LEFT',
    'правый ':  'RIGHT'
}

tech_condition_enum = {
    'б/у ' : 'beaten',
    'новый' : 'not_beaten'
}

gear_enum = {
    'постоянный полный ' : 'ALL_WHEEL_DRIVE',
    'передний ' : 'FORWARD_CONTROL',
    'задний ' : 'BACKWARD_CONTROL'
}

bodywork_enum = {
    'седан ': 'SEDAN',
    'купе ': 'COUPE',
    'хэтчбек ': 'HATCHBACK',
    'пикап ': 'PICKUP',
    'универсал ' : 'WAGON',
    'внедорожник ' : 'ALLROAD',
    'кроссовер ' : 'ALLROAD'
}



with open('irr.csv', 'a', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(names)

for i in range(1, get_pages(URL)+1):
    link_list = get_link_list_with_cards('https://irr.ru/cars/passenger/audi/page{}'.format(i))
    get_characteristics_with_page_to_CSV(link_list)






