# used_car_market_dataset
Posted public info on used cars for sale with key parameters.

# Dataset description
Dataset incudes key features placed on public sources with offers cars for sale. Data can be used for initializing non-trust offers cars for sale, clusterization of placed offers by features, identification of latent factors affect sales.

# Sources
Public placed offers on 5 popular sources with used cars offers in Russia:
- Drom.ru
- Auto.ru
- Avito.ru
- Youla.ru
- Irr.ru

# Repo structure
- README includes dataset detailed information on collection methods, features and others params.
- FOLDER DATA includes parsed data from all the sources.
- REQUIREMENTS includes libraries to work with.

# Data format
Parse data in format of json then merge and get .csv.

# Features placement

- производитель;brand
- модель;model
- год_выпуска;year
- пробег;mileage
- тип_двигателя;engine_type
- объем_двигателя;engine_capacity
- лошадиные_силы;horsepower
- привод;gear
- цвет;color
- тип_кузова;bodywork
- количество_дверей;doors_num
- руль;steering_wheel
- номер_кузова;vin
- владельцы_птс;owners_num
- состояние;tech_condition
