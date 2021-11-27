import sys
from importlib import import_module
from bokeh.io import export_png
from styles.utils import get_bokeh_theme, set_bokeh_theme

def create_graph(graph_object, graph_type, library):
    create_module = import_module('creators.{graph_type}'.format(graph_type=graph_type))
    creator_function_name = 'create_{library}_graph'.format(library=library)
    creator_function = getattr(create_module, creator_function_name)
    graph = creator_function(graph_object)
    return graph

def create_bokeh_graph(graph_type, graph):
    # generate and select bokeh theme
    theme = get_bokeh_theme()
    set_bokeh_theme(theme)
    # create graph based on graph_type
    generated_graph = [graph_type].create_bokeh_graph(graph)
    return generated_graph

def get_file_path(graph_type, library, id):
    return "../data/{graph_type}_{library}_{id}.png".format(
        graph_type=graph_type,
        library=library,
        id=id
    )

def export_graph(graph, library, filename):
    export_module = sys.modules[__name__]
    export_function_name = "export_{library}_graph".format(library=library)
    export_function = getattr(export_module, export_function_name)
    export_function(graph, filename)

def export_bokeh_graph(graph, filename):
    return None
    # export_png(graph, filename=filename)

def export_altair_graph(graph, filename):
    return None
    # graph.save(filename)

def export_plotnine_graph(graph, filename):
    return None
    # graph.save(filename=filename)