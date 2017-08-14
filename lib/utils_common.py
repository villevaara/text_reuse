import os


def create_dir_if_not_exists(directory_path):
    if not os.path.exist(directory_path):
        os.makedirs(directory_path)
