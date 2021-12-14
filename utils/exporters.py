import re
import json
import logging
import numpy as np
import holoviews as hv
from utils.utils import get_library_class

def export_graph_image(graph, library, file_path, regeneration=False):
    # provides a distinction in the logs between export and chart re-generation
    verb = 'Regenerating' if regeneration else 'Exporting'
    log_message('{verb} image {file_path}\n'.format(verb=verb, file_path=file_path))
    # render using holoviews (instead of native renderer)
    # used for libraries that don't support certain graph types
    if ('holoviews' in str(type(graph))):
        graph = hv.render(graph)
    
    export_class = get_library_class(library)
    export_class.export_graph(graph, file_path)

def export_graph_data(data, file_path):
    log_message('Exporting data {file_path}'.format(file_path=file_path))
    export_json(data, file_path)

def export_graph_styles(styles, file_path):
    log_message('Exporting styles {file_path}'.format(file_path=file_path))
    export_json(styles, file_path)

def export_json(content, file_path):
    serializable_content = convert_to_serializable(content)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(serializable_content, f, ensure_ascii=False, indent=4)

def convert_to_serializable(content):
    serialized_content = {}
    for key, value in content.items():
        serialized_value = serialize_value(value)
        serialized_content[key] = serialized_value
    return serialized_content

def serialize_value(value):
    serialized_value, value_type = value, type(value).__name__
    if (value_type == 'ndarray'):
        serialized_value = value.tolist()
    elif (value_type == 'list'):
        serialized_value = [serialize_value(val) for val in value]
    return serialized_value

def convert_from_serializable(content):
    serialized_content = {}
    for key, value in content.items():
        serialized_value = deserialize_value(value)
        serialized_content[key] = serialized_value
    return serialized_content

def deserialize_value(value):
    deserialized_value, value_type = value, type(value).__name__
    if (value_type == 'list'):
        deserialized_value = [deserialize_value(val) for val in value]
        # don't translate hex color codes to np array
        if(not isinstance(value[0], str) or not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value[0])):
            deserialized_value = np.array(deserialized_value)
    return deserialized_value

LOG_LEVEL = 50
def log_message(message):
    logging.log(LOG_LEVEL, message)