import sys
import json
import logging
import holoviews as hv

from altair_saver import save
from bokeh.io import export_png
from importlib import import_module
from styles.utils import get_bokeh_theme, set_bokeh_theme

def create_graph(graph_type, library, graph_object):
    create_module = import_module('creators.{graph_type}'.format(graph_type=graph_type))
    creator_function_name = 'create_{library}_graph'.format(library=library)
    creator_function = getattr(create_module, creator_function_name)
    graph = creator_function(graph_object)
    return graph

def create_bokeh_graph(graph_type, graph):
    print('LOL')
    set_bokeh_theme(get_bokeh_theme())
    generated_graph = [graph_type].create_bokeh_graph(graph)
    return generated_graph

def unpack_graph_object(graph_object):
    unpacked_object = (
        graph_object['data'],
        graph_object['styles'], 
    )
    return unpacked_object

def export_graph_data(data, file_path):
    log_message('Exporting data {file_path}'.format(file_path=file_path))
    export_json(data, file_path)

def export_graph_styles(styles, file_path):
    log_message('Exporting styles {file_path}'.format(file_path=file_path))
    export_json(styles, file_path)

def export_json(content, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

def export_graph_image(graph, library, file_path, regeneration=False):
    # provides a distinction in the logs between export and chart re-generation
    verb = 'Regenerating' if regeneration else 'Exporting'
    log_message('{verb} image {file_path}\n'.format(verb=verb, file_path=file_path))
    # render using holoviews (instead of native renderer)
    # used for libraries that don't support certain graph types
    if ('holoviews' in str(type(graph))):
        graph = hv.render(graph)
    
    export_module = sys.modules[__name__]
    export_function_name = 'export_{library}_graph'.format(library=library)
    export_function = getattr(export_module, export_function_name)
    export_function(graph, file_path)

def export_bokeh_graph(graph, file_path):
    export_png(graph, filename=file_path)

def export_altair_graph(graph, file_path):
    save(graph, file_path)

def export_plotnine_graph(graph, file_path):
    graph.save(file_path, verbose=False)

LOG_LEVEL = 50
def log_message(message):
    logging.log(LOG_LEVEL, message)