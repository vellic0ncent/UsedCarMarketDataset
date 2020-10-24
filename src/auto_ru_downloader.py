from bs4 import BeautifulSoup
import requests
import json
import csv
import random
import re
import os.path
import numpy as np
import webcolors

RGBS = np.empty((len(webcolors.CSS3_HEX_TO_NAMES), 3), dtype='int64')
COLOR_NAMES = []
for i, hex in enumerate(webcolors.CSS3_HEX_TO_NAMES):
    COLOR_NAMES.append(webcolors.CSS3_HEX_TO_NAMES[hex])
    RGBS[i] = webcolors.hex_to_rgb(hex)


def distance_with_many_vectors(vector_array, v):
    return np.sqrt(np.sum((vector_array - np.full(vector_array.shape, v)) ** 2, axis=1))


def soft_map_from_hex_to_name(hex):
    rgb = np.array(webcolors.hex_to_rgb(hex))
    color_distances = distance_with_many_vectors(RGBS, rgb)
    return COLOR_NAMES[color_distances.argmin()].upper()


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
        try:
            page_content = get_page_content(city, brand, page_num)
            offers = page_content['listing']['data']['offers']
            print(f"Auto.ru: page number: {page_num}, offers count: {len(offers)}")
            for offer in offers:
                id_to_offer[getOfferId(offer)] = offer
        except BaseException:
            print(f'Auto.ru: error during processing {page_num} page')


    print(f'Auto.ru: total offers downloaded: {len(id_to_offer)}')
    return id_to_offer


default_dump_filename = 'data/interim/auto_ru_cars'
default_example_dump_filename = 'data/interim/auto_ru_cars.example'


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


def extract_group_from_regexp(string: str, regexp: str) -> str:
    match = re.search(regexp, string)
    if match is not None:
        return match.group(1) or ''
    else:
        return ''


def map_offer_necessary_info(offer):
    try:
        return {
            'brand': offer['vehicle_info']['mark_info']['name'],
            'model': offer['vehicle_info']['model_info']['name'],
            'year': offer['documents']['year'],
            'price': offer['price_info']['price'],
            'mileage': offer['state']['mileage'],
            'horsepower': offer['vehicle_info']['tech_param']['power'],
            'engine_capacity': extract_group_from_regexp(
                offer['vehicle_info']['tech_param']['human_name'],
                '^(\d+.?\d*) '
            ),
            'engine_type': offer['vehicle_info']['tech_param']['engine_type'],
            'gear': offer['vehicle_info']['tech_param']['gear_type'],
            'transmission': extract_group_from_regexp(offer['vehicle_info']['tech_param']['human_name'], ' (\w+) \('),
            'bodywork': extract_group_from_regexp(offer['vehicle_info']['configuration']['body_type'], '^([A-Z]+)'),
            'doors_num': offer['vehicle_info']['configuration']['doors_count'],
            'steering_wheel': offer['vehicle_info']['steering_wheel'],
            'tech_condition': 'NOT_BEATEN' if offer['state']['state_not_beaten'] else 'BEATEN',
            'owners_num': offer['documents'].get('owners_number', 0),
            'vin': offer['documents'].get('vin', ''),
            'color': soft_map_from_hex_to_name(f"#{offer['color_hex']}")
        }
    except BaseException:
        print(f'Auto.ru: error during mapping offering with id {getOfferId(offer)}')
        return None


def map_offers_necessary_info(offers):
    return list(filter(lambda x: x is not None, map(map_offer_necessary_info, offers)))


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

