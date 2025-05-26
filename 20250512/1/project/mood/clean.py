import shutil
import os

def clean_targets():
    
    docs_build_dir = 'docs/build/html'
    if os.path.isdir(docs_build_dir):
        print(f'Removing directory {docs_build_dir} ...')
        shutil.rmtree(docs_build_dir)
    else:
        print(f'{docs_build_dir} does not exist.')

    pot_file = 'server/locale/messages.pot'
    if os.path.isfile(pot_file):
        print(f'Removing file {pot_file} ...')
        os.remove(pot_file)
    else:
        print(f'{pot_file} does not exist.')

    locale_dir = 'server/locale'
    for root, dirs, files in os.walk(locale_dir):
        for file in files:
            if file.endswith('.mo'):
                mo_path = os.path.join(root, file)
                print(f'Removing file {mo_path} ...')
                os.remove(mo_path)

    pytest_cache = '.pytest_cache'
    if os.path.isdir(pytest_cache):
        print(f'Removing directory {pytest_cache} ...')
        shutil.rmtree(pytest_cache)
    else:
        print(f'{pytest_cache} does not exist.')

    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                cache_path = os.path.join(root, dir_name)
                print(f'Removing directory {cache_path} ...')
                shutil.rmtree(cache_path)

if __name__ == '__main__':
    clean_targets()
