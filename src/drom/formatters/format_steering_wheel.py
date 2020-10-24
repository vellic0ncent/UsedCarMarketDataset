format_with = lambda mapper: lambda value: mapper.get(value.lower(), '')

steering_wheel_enum = {
    'левый': 'LEFT',
    'правый': 'RIGHT'
}

format_steering_wheel = format_with(steering_wheel_enum)