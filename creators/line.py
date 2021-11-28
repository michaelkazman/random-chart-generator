from bokeh.plotting import figure
from creators.utils import unpack_graph_object
import altair as alt
import pandas as pd
import numpy as np

parameters = {
    'width':    400,
    'height':   400,
    'colours': ['red', 'blue', 'green', 'orange', 'purple'],
    'matplot_marker': 'o',
    'bokeh_marker': "dot",
    'marker_size': 25,
}

def create_bokeh_graph(graph_object):
    # unpack data and create plot
    (X, y), style = unpack_graph_object(graph_object)
    p = figure(width=parameters['width'], height=parameters['height'])
    
    # draw each line individually
    for index, y_list in enumerate(y):
        colour = parameters['colours'][index]
        p.line(X, y_list, line_color = colour)
        getattr(p, parameters['bokeh_marker'])(X, y_list, line_color = colour, size=parameters['marker_size'])
    
    return p

def create_altair_graph(graph_object):
    # unpack data
    (X, y_lines), style = unpack_graph_object(graph_object)
    num_lines = len(y_lines)

    # create labels to group lines by
    line_names = np.copy(y_lines)
    for i in range(num_lines):
        line_names[i, :] = str(i)

    # format data to be appropriate for a data frame
    X = np.append(X, [X] * (num_lines - 1))
    y = y_lines.flatten()
    line_names = line_names.flatten()
    
    # create data frame
    source = pd.DataFrame({
        'x': X,
        'y': y,
        'line_names': line_names
    })

    # create line graph
    chart = alt.Chart(source).mark_line().encode(
        x = 'x',
        y = 'y',
        color = 'line_names',
    ).properties(
        width=parameters['width'],
        height=parameters['height'],
    )
    return chart

def create_plotnine_graph(graph_object):
    # unpack data
    (X, y), style = unpack_graph_object(graph_object)
    return {}