def setup_graph():
    return None

def get_theme():
    return 'caliber'

def set_theme(theme):
    return None

def export_graph(graph, file_path):
    graph.save(file_path, verbose=False)