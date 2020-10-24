format_with = lambda mapper: lambda value: mapper.get(value.lower(), '')

bodywork_enum = {
    'седан': 'SEDAN',
    'джип/suv 3 дв.': 'ALLROAD',
    'джип/suv 5 дв.': 'ALLROAD',
    'минивэн': 'WAGON',
    'купе': 'COUPE',
    'хэтчбек 3 дв.': 'HATCHBACK',
    'хэтчбек 5 дв.': 'HATCHBACK',
    'открытый': 'CABRIO',
    'пикап': 'PICKUP',
    'лифтбэк': 'LIFTBACK'
}

format_bodywork = format_with(bodywork_enum)