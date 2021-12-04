import sys
import json
import logging
import holoviews as hv

from importlib import import_module

def export_graph_image(graph, library, file_path, regeneration=False):
    # provides a distinction in the logs between export and chart re-generation
    verb = 'Regenerating' if regeneration else 'Exporting'
    log_message('{verb} image {file_path}\n'.format(verb=verb, file_path=file_path))
    # render using holoviews (instead of native renderer)
    # used for libraries that don't support certain graph types
    if ('holoviews' in str(type(graph))):
        graph = hv.render(graph)
    
    export_module = import_module('libraries.{library}'.format(library=library))
    export_function_name = 'export_graph'.format(library=library)
    export_function = getattr(export_module, export_function_name)
    export_function(graph, file_path)

def export_graph_data(data, file_path):
    log_message('Exporting data {file_path}'.format(file_path=file_path))
    export_json(data, file_path)

def export_graph_styles(styles, file_path):
    log_message('Exporting styles {file_path}'.format(file_path=file_path))
    export_json(styles, file_path)

def export_json(content, file_path):
    serializable_content = convert_to_serializable(content)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

def convert_to_serializable(content):
    serialized_content = {}
    for key, value in content.items():
        serialized_value, value_type = value, type(value)
        if (value_type == 'numpy.ndarray'):
            serialized_value = value.tolist()

        serialized_content[key] = serialized_value
    return serialized_content

LOG_LEVEL = 50
def log_message(message):
    logging.log(LOG_LEVEL, message)