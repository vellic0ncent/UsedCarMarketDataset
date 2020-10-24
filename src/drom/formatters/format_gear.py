format_with = lambda mapper: lambda value: mapper.get(value.lower(), '')

gear_enum = {
    '4wd': 'ALL_WHEEL_DRIVE',
    'передний': 'FORWARD_CONTROL',
    'задний': 'BACKWARD_CONTROL'
}

format_gear = format_with(gear_enum)