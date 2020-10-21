from bs4 import BeautifulSoup
import requests
import json
import csv
import random
import os.path


def getOfferId(offer: dict) -> str:
    return f"{offer['id']}-{offer['hash']}"


def construct_url_for(city: str, brand: str) -> str:
    if brand == 'all':
        return f'https://auto.ru/{city}/cars/all/'
    else:
        return f'https://auto.ru/{city}/cars/{brand}/all/'


request_default_params = {'output_type': 'list', 'sort': 'cr_date-desc'}


def get_page_content(city: str, brand: str, page_num: int) -> dict:
    url = construct_url_for(city, brand)
    request_params = request_default_params.copy()
    request_params['page'] = page_num
    page_content = requests.get(url, params=request_params).content
    soup = BeautifulSoup(page_content, 'html.parser')
    initial_state_tag = soup.find('script', {'id': 'initial-state'})
    return json.loads(initial_state_tag.string)


def download_raw_offers(city='moskva', brand='all', page_count=100) -> dict:
    id_to_offer = {}
    for page_num in range(1, page_count):
        page_content = get_page_content(city, brand, page_num)
        offers = page_content['listing']['data']['offers']
        print(f"Auto.ru: page number: {page_num}, offers count: {len(offers)}")
        for offer in offers:
            id_to_offer[getOfferId(offer)] = offer
    print(f'Auto.ru: total offers downloaded: {len(id_to_offer)}')
    return id_to_offer


default_dump_filename = 'data/auto_ru_cars'
default_example_dump_filename = 'data/auto_ru_cars.example'


def dump_offers_to_file_as_json(id_to_offer: dict, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(id_to_offer, f)


def dump_some_examples_to_file_as_json(id_to_offer: dict,
                                       filename: str,
                                       examples_count=5) -> dict:
    id_to_offer_examples = {offer_id: offer for offer_id, offer in random.sample(id_to_offer.items(), examples_count)}
    dump_offers_to_file_as_json(id_to_offer_examples, filename)
    return id_to_offer_examples


def read_offers(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def map_offer_necessary_info(offer):
    return {
        'brand': offer['vehicle_info']['mark_info']['name'],
        'model': offer['vehicle_info']['model_info']['name'],
        'year': offer['documents']['year'],
        'mileage': offer['state']['mileage'],
        'engine_type': offer['vehicle_info']['tech_param']['engine_type'],
        'transmission': offer['vehicle_info']['tech_param']['gear_type'],
        'color': offer['color_hex'],
        'bodywork': offer['vehicle_info']['configuration']['body_type'],
        'doors_num': offer['vehicle_info']['configuration']['doors_count'],
        'steering_wheel': offer['vehicle_info']['steering_wheel'],
        'vin': offer['documents'].get('vin', None),
        'owners_num': offer['documents'].get('owners_number', 0),
        'tech_condition': 'NOT_BEATEN' if offer['state']['state_not_beaten'] else 'BEATEN',
        'horsepower': offer['vehicle_info']['tech_param']['power'],
        'engine_capacity': offer['vehicle_info']['tech_param']['human_name'],
        'price': offer['price_info']['price'],
        'price_currency': offer['price_info']['currency'],
        'price_with_nds': offer['price_info']['with_nds']
    }


def map_offers_necessary_info(offers):
    return list(map(map_offer_necessary_info, offers))


def dump_offers_to_file_as_csv(offers: list, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, offers[0].keys(), delimiter=',')
        writer.writeheader()
        writer.writerows(offers)


def upload_auto_ru_dataset(city: str,
                           brand: str,
                           filename=default_dump_filename,
                           examples_filename=default_example_dump_filename,
                           page_count=100,
                           use_cache=True,
                           save_example=True) -> None:
    full_info_offer_filename = f'{filename}.json'
    if use_cache and os.path.isfile(full_info_offer_filename):
        print('Auto.ru: reading offers from cache')
        id_to_offer = read_offers(full_info_offer_filename)
    else:
        print(f'Auto.ru: downloading offers for {city} and {brand}')
        id_to_offer = download_raw_offers(city, brand, page_count)
        print(f'Auto.ru: saving downloaded offers to {full_info_offer_filename}')
        dump_offers_to_file_as_json(id_to_offer, full_info_offer_filename)
    if save_example:
        full_info_offer_examples_filename = f'{examples_filename}.json'
        id_to_offer_examples = dump_some_examples_to_file_as_json(id_to_offer, full_info_offer_examples_filename)
    mapped_offers_filename = f'{filename}.csv'
    print(f'Auto.ru: saving mapped offers to {mapped_offers_filename}')
    dump_offers_to_file_as_csv(map_offers_necessary_info(id_to_offer.values()), mapped_offers_filename)
    if save_example:
        dump_offers_to_file_as_csv(map_offers_necessary_info(id_to_offer_examples.values()), f'{examples_filename}.csv')

