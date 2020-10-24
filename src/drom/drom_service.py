import requests

_brand_url = 'https://www.drom.ru/'

def _get_html(url):
    response = requests.get(url)
    return response.content

def _make_cars_url(city, brand, page_number): 
    return f'https://{city}.drom.ru/{brand}/all/page{page_number}/'

def get_brands_html():
    html = _get_html(_brand_url)
    return html

def get_cars_html(options):
    url = _make_cars_url(options['city'], options['brand'], options['page_number'])
    html = _get_html(url)
    return html

def get_car_html(url):
    html = _get_html(url)
    return html