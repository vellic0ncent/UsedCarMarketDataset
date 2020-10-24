import pandas as pd


if __name__ == '__main__':
    auto_ru = pd.read_csv('data/interim/auto_ru_cars.csv')
    avito = pd.read_csv('data/interim/avito.csv')
    drom = pd.read_csv('data/interim/drom.csv')
    irr = pd.read_csv('data/interim/irr.csv')
    youla = pd.read_csv('data/interim/youla.csv')
    all = pd.concat([auto_ru, avito, drom, irr, youla], ignore_index=True, sort=False)
    print(f'Length of concatenated dataset: {all.shape[0]}')
    columns_identifiers = ['brand', 'model', 'year', 'price', 'mileage', 'horsepower', 'engine_capacity', 'engine_type',
                           'gear', 'transmission', 'bodywork', 'doors_num', 'steering_wheel', 'tech_condition']
    all = all.drop_duplicates(subset=columns_identifiers)
    print(f'Length of dataset with removed duplicates: {all.shape[0]}')
    all_filename = 'data/result.csv'
    all.to_csv('data/result.csv', index=False, columns=all.columns, encoding='utf-8')
    print(f"Merged dataset is saved to '{all_filename}'")