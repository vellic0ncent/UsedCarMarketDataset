import requests
import csv
import sys

from drom.columns.columns_csv import columns_csv
import drom.drom_service as service
import drom.drom_parser as parser
import drom.prepare2serilalize as p2s

def parse_drom(into, city, brand, record_num = sys.maxsize):
    with open(into, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns_csv)
        writer.writeheader()
        records_parsed = 0
        for page_number in range(record_num):
            print(f'Parsing {page_number + 1} page...')
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
                    prepared2serialize = p2s.prepare2serialize(car)
                    writer.writerow(prepared2serialize)
                    records_parsed += 1
                    print(f'Records parsed: {records_parsed}')
                    if (records_parsed == record_num):
                        return
                except Exception as e:
                    print('Exception during serializing: ', e)
                    continue