def format_price(value):
    return int(''.join(value.split('\xa0')[0:-1]))