import os
import json
import numpy as np
from utils.utils import json_from_file, get_files_from_dir, get_module_attr

# get list of themes (excluding python system files)
def get_themes(dir):
    theme_dir = 'themes/{dir}'.format(dir=dir)
    themes = get_files_from_dir(theme_dir)
    return themes

# pick random theme from a libraries theme list
def get_random_theme(dir):
    themes = get_themes(dir)
    theme_file_name = np.random.choice(themes)
    return theme_file_name

# read in a theme from a libraries theme directory
def get_theme_object(file_path, dir):
    file_name, file_extension = os.path.splitext(file_path)
    theme = {}
    # json theme objects
    if file_extension == '.json':
        theme =  json_from_file('themes/{dir}/{file_path}'.format(file_path=file_path, dir=dir))
    # class-based themes
    elif file_extension == '.py':
        theme_class = get_module_attr('themes.{dir}.{file_name}'.format(dir=dir, file_name=file_name), 'Theme')
        theme = theme_class
    return theme
