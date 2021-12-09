import os
import altair as alt
from altair_saver import save

from utils.libraries import get_themes, get_random_theme, get_theme_object
from libraries.library import Library as BaseLibrary

class Library(BaseLibrary):
    def setup_hook():
        themes = get_themes('altair')
        for theme in themes:
            theme_object = get_theme_object(theme, 'altair')
            alt.themes.register(theme, lambda: theme_object)

    def get_theme():
        theme_file_path = get_random_theme('altair')
        return theme_file_path

    def set_theme(graph_type, theme):
        alt.themes.enable(theme)

    def export_graph(graph, file_path):
        save(graph, file_path)