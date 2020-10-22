import requests
from bs4 import BeautifulSoup
import csv
from functools import reduce

extract_html_node_attr = lambda attr: lambda html_node: html_node.get(attr)
extract_html_node_value = lambda html_node: html_node.get_text() 
make_cars_url = lambda city, brand, page_number: f'https://{city}.drom.ru/{brand}/all/page{page_number}/'

class DromService:
    _brand_url = 'https://www.drom.ru/'

    def get_brands_html(self):
        html = self._get_html(self._brand_url)
        return html

    def get_cars_html(self, options):
        url = self._make_cars_url(options['city'], options['brand'], options['page_number'])
        html = self._get_html(url)
        return html

    def get_car_html(self, url):
        html = self._get_html(url)
        return html

    def _get_html(self, url):
        response = requests.get(url)
        return response.content

    def _make_cars_url(self, city, brand, page_number): 
        return f'https://{city}.drom.ru/{brand}/all/page{page_number}/'

class DromParser:
    def parse_car(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        car = {}
        car['Модель'] = extract_html_node_value(soup.find('h1', {'class': 'css-cgwg2n e18vbajn0'}))
        car['Цена'] = extract_html_node_value(soup.find('div', {'class': 'css-1hu13v1 e162wx9x0'}))
        params = list(
            map(
                extract_html_node_value,
                soup.find_all('th', {'class': 'css-k5ermf ezjvm5n0'})
            )
        )
        param_values = list(
            map(
                extract_html_node_value,
                soup.find_all('td', {'class': 'css-1uz0iw8 ezjvm5n1'})
            )
        )
        for param, param_value in zip(params, param_values):
            car[param] = param_value

        return car

    def parse_cars_urls(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        attr_extracter = extract_html_node_attr('href')
        return list(
            map(
                attr_extracter,
                soup.find_all('a', {
                    'data-ftid': 'bulls-list_bull'
                })
            )
        )

    def parse_car_brands(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return list(
            map(
                extract_html_node_value, 
                soup.find_all('a', {
                    'class':'css-171rdfx ebqjjri2'
                    }
                )
            )
        )

class CsvSerializer:
    def __init__(self, into, columns):
        self.filePath = into
        self.columns = columns

    def serialize(self, transaction):
        with open(self.filePath, 'w') as csvfile:
            self.writer = csv.DictWriter(csvfile, fieldnames=self.columns)
            self.writer.writeheader()
            transaction(self)

    def write(self, data):
        self.writer.writerow(data)

columns_drom = [
    'Модель', 
    'Цена',
    'Двигатель',
    'Мощность',
    'Трансмиссия',
    'Привод',
    'Тип кузова',
    'Цвет',
    'Пробег',
    'Пробег, км',
    'Руль',
    'Поколение',
    'Комплектация',
    'VIN',
    'Особые отметки'
]

columns_csv = [
    'Brand',
    'Model',
    'Price',
    'Year',
    'Mileage',
    'Engine_type',
    'Transmission',
    'Color',
    'Bodywork',
    'Doors_num',
    'Steering_wheel',
    'Vin',
    'Owners_num',
    'Tech_condition',
    'Horsepower',
    'Engine_capacity'
]

def prepare2serialize(car):
    prepared_car = {}
    arr_model = car['Модель'].split(',')
    prepared_car['Brand'] = arr_model[0].split(' ')[1]
    prepared_car['Model'] = arr_model[0].split(' ')[2]
    prepared_car['Year'] = arr_model[1].split(' ')[0]
    prepared_car['Price'] = car['Цена']
    mileage = (
        car['Пробег'] if 'Пробег' in car 
        else car['Пробег, км'] if 'Пробег, км' in car else '')

    prepared_car['Mileage'] = 0 if mileage == 'новый автомобиль' else mileage
    if 'Двигатель' in car:
        arr_engine = car['Двигатель'].split(', ')
        prepared_car['Engine_type'] = arr_engine[0]
        prepared_car['Engine_capacity'] = arr_engine[1].split(' ')[0]

    if 'Трансмиссия' in car:
        prepared_car['Transmission'] = car['Трансмиссия']

    if 'Цвет' in car:
        prepared_car['Color'] = car['Цвет']

    if 'Тип кузова' in car:
        prepared_car['Bodywork'] = car['Тип кузова']

    if 'Руль' in car:
        prepared_car['Steering_wheel'] = car['Руль']

    if 'Мощность' in car:
        prepared_car['Horsepower'] = car['Мощность'].split(' ')[0].split(' ')[0]

    return prepared_car

def parse_drom(into, city):
    service = DromService()
    parser = DromParser()
    serializer = CsvSerializer(into, columns_csv)
    brands_html = service.get_brands_html()
    brands = parser.parse_car_brands(brands_html)
    def transaction(serializer):
        for brand in brands:
            page_number = 1
            while(True):
                print(f'Parsing {page_number} page...')
                cars_page_html = service.get_cars_html({
                    'city': city, 
                    'brand': brand.lower(), 
                    'page_number': page_number
                })
                cars_urls = parser.parse_cars_urls(cars_page_html)
                if len(cars_urls) == 0: break

                for car_url in cars_urls:
                    try:
                        car_html = service.get_car_html(car_url)
                        car = parser.parse_car(car_html)
                        prepared2serialize = prepare2serialize(car)
                        serializer.write(prepared2serialize)
                    except Exception:
                        print('Exception!')
                        continue

                page_number += 1

    serializer.serialize(transaction)

parse_drom("drom.csv", "moscow")