from importlib import import_module
from bokeh.io import curdoc

def generate_styles(graph_type, library):
    stylize_module = import_module('styles.{graph_type}'.format(graph_type=graph_type))
    stylize_function_name = 'generate_{library}_styles'.format(library=library)
    stylize_function = getattr(stylize_module, stylize_function_name)
    styles = stylize_function()
    return styles

def get_bokeh_theme():
    return 'caliber'

def set_bokeh_theme(theme):
    curdoc().theme = theme

def get_altair_theme():
    # TODO
    return None

def set_altair_theme():
    # TODO
    return None

def set_altair_theme():
    # TODO
    return None

def get_plotnine_theme():
    # TODO
    return None
