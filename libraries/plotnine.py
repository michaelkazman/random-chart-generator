import plotnine as p9
from utils.libraries import get_theme_object
from libraries.library import Library as BaseLibrary

class Library(BaseLibrary):
    def set_theme(graph_type, theme):
        theme = get_theme_object(theme, 'plotnine')
        p9.theme_set(theme)
    
    def export_graph(graph, file_path):
        graph.save(file_path, verbose=False)