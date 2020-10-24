def format_mileage(mileage):
    return 0 if mileage == 'новый автомобиль' else int(''.join(mileage.split(' ')))