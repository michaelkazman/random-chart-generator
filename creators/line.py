from bokeh.plotting import figure
from creators.utils import unpack_graph_object

parameters = {
    'x_end':    400,
    'height':   400,
    'colours': ['red', 'blue', 'green', 'orange', 'purple'],
    'matplot_marker': 'o',
    'bokeh_marker': "dot",
    'marker_size': 25,
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y), style = unpack_graph_object(graph_object)
    p = figure(width=parameters['x_end'], height=parameters['height'])
    
    # go through each layer and draw it as a separate line
    for index, y_list in enumerate(y):
        colour = parameters['colours'][index]
        p.line(X, y_list, line_color = colour)
        getattr(p, parameters['bokeh_marker'])(X, y_list, line_color = colour, size=parameters['marker_size'])
    
    return p

def create_altair_graph(graph_object):
    return {}

def create_plotnine_graph(graph_object):
    return {}