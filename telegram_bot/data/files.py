
from django.conf import settings


DATA_FILES = {

    'test_data': {
        't_user': 't_user.csv',
        'score': 'score.csv',
        'marketplase': 'marketplase.csv',
        'product': 'product.csv'
    },

    'data': {
        't_user': 't_user.csv',
    }
}

def get_path_to_file(name,file):
    clear_name = name.split('.')[3]
    return settings.DATA_ROOT / DATA_FILES[clear_name][file]
