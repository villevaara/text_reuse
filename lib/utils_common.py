import os
from datetime import datetime


def create_dir_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def get_current_date_string():
    datestring = datetime.now().strftime('%y%m%d')
    return datestring
