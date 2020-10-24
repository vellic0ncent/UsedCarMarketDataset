import auto_ru_downloader
from drom.parse_drom import parse_drom

if __name__ == '__main__':
    auto_ru_downloader.upload_auto_ru_dataset('moskva', 'audi', use_cache=True)
    parse_drom(into="drom.csv", city='moscow', brand='audi', record_num=500)
    print('Downloading datasets is done!')
