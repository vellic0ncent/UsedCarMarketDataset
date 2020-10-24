format_with = lambda mapper: lambda value: mapper.get(value.lower(), '')

engine_type_enum = {
    'дизель': 'DIESEL',
    'бензин': 'GASOLINE',
    'электро': 'ELECTRO',
    'гибрид': 'HYBRID'
}

format_engine_type = format_with(engine_type_enum)