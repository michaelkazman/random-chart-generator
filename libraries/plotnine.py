from altair.vegalite.v4 import theme
import plotnine as p9
from utils.libraries import get_random_theme, get_theme_object
from libraries.library import Library as BaseLibrary

class Library(BaseLibrary):
    def get_theme():
        theme_file_path = get_random_theme('plotnine')
        return theme_file_path

    def set_theme(theme):
        theme = get_theme_object(theme, 'plotnine')
        p9.theme_set(theme)
    
    def export_graph(graph, file_path):
        graph.save(file_path, verbose=False)