format_with = lambda mapper: lambda value: mapper.get(value.lower(), '')

transmission_enum = {
    'робот': 'AMT',
    'автомат': 'AT',
    'вариатор': 'CVT',
    'механика': 'MT'
}

format_transmission = format_with(transmission_enum)