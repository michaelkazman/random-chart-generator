import os
import json
from importlib import import_module

# get files from dir (excluding python sys files)
def get_files_from_dir(dir, exclusions=['__init__.py', '__pycache__']):
    dir_files = os.listdir(dir)
    files = [file for file in dir_files if file not in exclusions]
    return files

# retrieve json from file
def json_from_file(file_path):
    with open(file_path) as f:
      return json.load(f)

# get attribute from module in the project
def get_module_attr(module_name, attribute_name):
    module = import_module(module_name)
    attribute = getattr(module, attribute_name)
    return attribute
    
# get class from library file based on file name
def get_library_class(library):
    library_class = get_module_attr('libraries.{library}'.format(library=library), 'Library')
    return library_class