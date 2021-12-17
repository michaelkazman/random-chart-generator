from utils.libraries import get_random_theme

class Library():
    # occurs before any generation is run
    # used as a setup / initialization step
    def setup_hook():
        pass

    # occurs before the creation is run
    # typically includes setup like setting the theme, etc.
    def pre_creation_hook():
        pass
    
    # retrieves the theme from the corresponding directory
    def get_theme(theme):
        theme_file_path = get_random_theme(theme)
        return theme_file_path

    # sets the theme 
    def set_theme(graph_type, theme):
        raise NotImplementedError

    # occurs after the creation is run, passes in the graph
    # in case any modifications are needed
    def post_creation_hook(graph_type, graph):
        pass

    # exports the provided graph to the specified file path
    def export_graph(graph, file_path):
        raise NotImplementedError

