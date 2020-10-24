import re

kI = lambda x: x

extract_bodywork = kI
extract_color = kI
extract_gear = kI
extract_mileage = kI
extract_price = kI
extract_steering_wheel = kI
extract_transmission = kI

def extract_engine_capacity(value):
    return value.split(', ')[1].split(' ')[0]

def extract_brand(value):
    return value.split(',')[0].split(' ')[1]

def extract_engine_type(value):
    return value.split(', ')[0]

def extract_hoursepower(value):
    return int(re.search(r'[0-9]*', value).group(0))

def extract_model(value): 
    return value.split(',')[0].split(' ')[2]

def extract_vin(value):
    return value.split(' ')[0].split(' ')[0]

def extract_year(value):
    return value.split(', ')[1].split(' ')[0]

def extract_doors_num(value):
    match = re.search(r'[0-9]+', value)
    if match is None:
        return 4 if value == 'универсал' or value == 'минивэн' else 2

    return match.group(0)