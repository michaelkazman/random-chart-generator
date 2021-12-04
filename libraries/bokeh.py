from bokeh.io import export_png, curdoc

def setup_graph():
    set_theme(get_theme())

def get_theme():
    return 'caliber'

def set_theme(theme):
    curdoc().theme = theme

def export_graph(graph, file_path):
    export_png(graph, filename=file_path)