from bokeh.plotting import figure
from creators.utils import unpack_graph_object
import altair as alt
import pandas as pd
import numpy as np

parameters = {
    'width':    400,
    'height':   400,
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
        p.line(X, y_list)
        getattr(p, parameters['bokeh_marker'])(X, y_list, size=parameters['marker_size'])
    
    return p

def create_altair_graph(graph_object):
    # unpack data
    (X, y), style = unpack_graph_object(graph_object)

    # for each layer, make data frame and store its line graph
    layered_lines = []
    for i in range(0, len(y)):
        source = pd.DataFrame({"x": X, "y": y[i]})
        lines = alt.Chart(source).mark_line().encode(
            x='x',
            y='y',
        )
        layered_lines.append(lines)
    
    # make final chart by layering
    chart = alt.layer(*layered_lines)
    return chart

def create_plotnine_graph(graph_object):
    # unpack data
    (X, y), style = unpack_graph_object(graph_object)
    return {}