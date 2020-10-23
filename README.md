# Dataset USED CAR MARKET
Posted public info on used cars for sale with key parameters.

### About
Dataset incudes key features placed on public sources with offers cars for sale. Data can be used for initializing non-trust offers cars for sale, clusterization of placed offers by features, identification of latent factors affect sales.

### Sources
Public placed offers on 5 popular sources with used cars offers in Russia:
1. http://Drom.ru
2. http://Auto.ru
3. http://Avito.ru
4. http://Youla.ru
5. http://Irr.ru

### Repo structure
1) */data* includes folder "interim" and integrated result from the folder "interim" in .csv format
2) */data/interim* includes raw data got by 5 parsers in .csv format
3) *scr* ncludes 5 parsers in .py format and integrator main.py
4) *README* includes dataset detailed information on collection methods, features and others params.

### Data collection methods and formating
Parse data on the main page, get into the offer for the detailed information transfer through all the pages. Pre-process of the data integration is to unify the measures and values, all in all format to get RAW DATA (/data/interim/). Some aspects need to consider, f.e.: "color" parameter unify - hex transformation (auto.ru) and translation of color name from ru to eng for other sources. Data integration step includes merge info from all the sources.

### Features placement
Features are based on 3 blocks - car identity, technical parameters, figure (build) parameters and others. All the detailed information is placed below.

##### Characteristics for car identify:

`brand [производитель]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
str | AUDI | Identified by user | -

`model [модель]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
str | A3-A8, Q3-Q8 and others | - | -

`year [год выпуска]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
int | 1960 - 2020 | - | year

`price [цена]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
int | 0 + | - | RUB w/o VAT

`mileage [пробег]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
int | 0 + | - | km

##### Technical parameters for car identify:

`horsepower [лошадиные силы]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
int | 0 + | - | hp

`engine_capacity [крутящий момент двигателя]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
float | 0 + | - | nm

`engine_type [тип двигателя]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
str | DIESEL, GASOLINE, ELECTRO, HYBRID | дизель, бензин, электро, гибрид | -

`gear [привод]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
str | ALL_WHEEL_DRIVE, FORWARD_CONTROL, BACKWARD_CONTROL | полный, передний, задний | -

`transmission [трансмиссия]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
str | AMT, AT, CVT, MT | Робот, автомат, вариатор, механика | -

##### Figure (build) parameters for car identify:

`bodywork [тип кузова]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
str | SEDAN, ALLROAD, WAGON, COUPE, HATCHBACK, CABRIO, PICKUP, LIFTBACK | Седан, внедорожник (джип), универсал (минивэн), купе, хэтчбек, кабриолет (открытый), пикап, лифтбэк | -

`doors_num [количество дверей]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
int | 2 - 6 | - | pcs

`steering_wheel [руль]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
str | LEFT RIGHT | - | -

`tech_conditions [техническое состояние]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
str | BEATEN NOT_BEATEN | Битый, не битый | -

##### Other parameters for car identify:

`owners_num [количество владельцев по ПТС]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
int | 0 + | - | ppl

`vin [ВИН]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
str | - | - | -

`color [цвет]`
Type | Valid values | Comment | Units
--- | --- | --- | ---
str | BLACK, WHITE, BROWN and others | - | -
