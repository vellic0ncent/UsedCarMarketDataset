import auto_ru_downloader

if __name__ == '__main__':
    auto_ru_downloader.upload_auto_ru_dataset('moskva', 'audi', use_cache=False)
    print('Downloading datasets is done!')
