from bokeh.themes import Theme
from bokeh.io import export_png, curdoc
from utils.libraries import get_random_theme, get_theme_object
from libraries.library import Library as BaseLibrary

class Library(BaseLibrary):
    def get_theme():
        theme_file_path = get_random_theme('bokeh')
        return theme_file_path

    def set_theme(theme):
        theme_json = get_theme_object(theme, 'bokeh')
        theme_object = Theme(json=theme_json)
        curdoc().theme = theme_object
    
    def post_creation_hook(graph):
        curdoc().add_root(graph)

    def export_graph(graph, file_path):
        export_png(graph, filename=file_path)