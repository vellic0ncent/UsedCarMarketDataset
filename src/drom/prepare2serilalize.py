import extracters as e

from formatters.format_gear import format_gear
from formatters.format_bodywork import format_bodywork
from formatters.format_transmission import format_transmission
from formatters.format_color import format_color
from formatters.format_engine_type import format_engine_type
from formatters.format_steering_wheel import format_steering_wheel
from formatters.format_mileage import format_mileage
from formatters.format_price import format_price

from no_throw import no_throw

prepare_model = lambda v: e.extract_model(v)
prepare_brand = lambda v: e.extract_brand(v)
prepare_year = lambda v: e.extract_year(v)
prepare_price = lambda v: format_price(e.extract_price(v))
prepare_color = lambda v: format_color(e.extract_color(v))
prepare_gear = lambda v: format_gear(e.extract_gear(v))
prepare_transmission = lambda v: format_transmission(e.extract_transmission(v))
prepare_bodywork = lambda v: format_bodywork(e.extract_bodywork(v))
prepare_steering_wheel = lambda v: format_steering_wheel(e.extract_steering_wheel(v))
prepare_hoursepower = lambda v: e.extract_hoursepower(v)
prepare_vin = lambda v: e.extract_vin(v)
prepare_engine_type = lambda v: format_engine_type(e.extract_engine_type(v))
prepare_engine_capacity = lambda v: e.extract_engine_capacity(v)
prepare_mileage = lambda v: format_mileage(e.extract_mileage(v))
prepare_doors_num = lambda v: e.extract_doors_num(v)

def prepare2serialize(car):
    prepared_car = {}
    prepared_car['model'] = no_throw(lambda: prepare_model(car['Модель']), '')
    prepared_car['brand'] = no_throw(lambda: prepare_brand(car['Модель']), '')
    prepared_car['year'] = no_throw(lambda: prepare_year(car['Модель']), '')
    prepared_car['price'] = no_throw(lambda: prepare_price(car['Цена']), '')
    prepared_car['color'] = no_throw(lambda: prepare_color(car['Цвет']), '')
    prepared_car['gear'] = no_throw(lambda: prepare_gear(car['Привод']), '')
    prepared_car['transmission'] = no_throw(lambda: prepare_transmission(car['Трансмиссия']), '')
    prepared_car['bodywork'] = no_throw(lambda: prepare_bodywork(car['Тип кузова']), '')
    prepared_car['steering_wheel'] = no_throw(lambda: prepare_steering_wheel(car['Руль']), '')
    prepared_car['horsepower'] = no_throw(lambda: prepare_hoursepower(car['Мощность']), '')
    prepared_car['vin'] = no_throw(lambda: prepare_vin(car['VIN']), '')
    prepared_car['engine_type'] = no_throw(lambda: prepare_engine_type(car['Двигатель']), '')
    prepared_car['engine_capacity'] = no_throw(lambda: prepare_engine_capacity(car['Двигатель']), '')
    prepared_car['doors_num'] = no_throw(lambda: prepare_doors_num(car['Тип кузова']), '')
    prepared_car['mileage'] = (
        prepare_mileage(car['Пробег']) if 'Пробег' in car 
        else prepare_mileage(car['Пробег, км']) if 'Пробег, км' in car else '')

    return prepared_car