import sys
from importlib import import_module
from bokeh.io import export_png
from altair_saver import save
import holoviews as hv
from styles.utils import get_bokeh_theme, set_bokeh_theme
import logging

def create_graph(graph_type, library, graph_object):
    create_module = import_module('creators.{graph_type}'.format(graph_type=graph_type))
    creator_function_name = 'create_{library}_graph'.format(library=library)
    creator_function = getattr(create_module, creator_function_name)
    graph = creator_function(graph_object)
    return graph

def create_bokeh_graph(graph_type, graph):
    print("LOL")
    set_bokeh_theme(get_bokeh_theme())
    generated_graph = [graph_type].create_bokeh_graph(graph)
    return generated_graph

def get_file_name(graph_type, library, id):
    return '{graph_type}_{library}_{id}'.format(
        graph_type=graph_type,
        library=library,
        id=id
    )

def get_file_path(file_name, path, file_type):
    return 'output/{path}/{file_name}.{file_type}'.format(
        file_name=file_name,
        path=path,
        file_type=file_type
    )

def unpack_graph_object(graph_object):
    unpacked_object = (
        graph_object['data'],
        graph_object['styles'], 
    )
    return unpacked_object

def export_graph_data(data, file_path):
    log_message('Exporting data {file_path}'.format(file_path=file_path))
    # do stuff

def export_graph_styles(styles, file_path):
    log_message('Exporting styles {file_path}'.format(file_path=file_path))
    # do stuff

def export_graph_image(graph, library, file_path, verbose=True):
    log_message('Exporting images {file_path}\n'.format(file_path=file_path))
    # render using holoviews (instead of native renderer)
    # used for libraries that don't support certain graph types
    if ('holoviews' in str(type(graph))):
        graph = hv.render(graph)
    
    export_module = sys.modules[__name__]
    export_function_name = "export_{library}_graph".format(library=library)
    export_function = getattr(export_module, export_function_name)
    export_function(graph, file_path)

def export_bokeh_graph(graph, filename):
    export_png(graph, filename=filename)

def export_altair_graph(graph, filename):
    save(graph, filename)

def export_plotnine_graph(graph, filename):
    return None
    # graph.save(filename=filename)

LOG_LEVEL = 50
def log_message(message):
    logging.log(LOG_LEVEL, message)