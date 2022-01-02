import altair as alt
from altair_saver import save
from libraries.library import Library as BaseLibrary
from utils.libraries import get_themes, get_theme_object

class Library(BaseLibrary):
    def setup_hook():
        themes = get_themes('altair')
        for theme in themes:
            theme_object = get_theme_object(theme, 'altair')
            alt.themes.register(theme, lambda n=theme_object: n)

    def set_theme(graph_type, theme):
        alt.themes.enable(theme)

    def export_graph(graph, file_path):
        save(graph, file_path)