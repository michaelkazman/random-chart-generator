import altair as alt
import pandas as pd
import numpy as np
import plotnine as p9

from bokeh.plotting import figure
from utils.creators import convert_numbers_to_letters, unpack_graph_object

parameters = {
    'width':    400,
    'height':   400,
    'matplot_marker': 'o',
    'bokeh_marker': 'dot',
    'marker_size': 25,
}

def create_bokeh_graph(graph_object):
    # unpack data and create plot
    (X, y, *_), styles = unpack_graph_object(graph_object)
    p = figure(
        width=parameters.get('width'),
        height=parameters.get('height'),
        x_axis_label='X',
        y_axis_label='y',
        toolbar_location=None,
    )
    
    # draw each line individually
    for _, y_list in enumerate(y):
        p.line(X, y_list)
        getattr(p, parameters['bokeh_marker'])(X, y_list, size=parameters['marker_size'])
    
    return p

def create_altair_graph(graph_object):
    # unpack data
    (X, y, *_), styles = unpack_graph_object(graph_object)

    # for each layer, make data frame and store its line graph
    layered_lines = []
    for i in range(0, len(y)):
        df = pd.DataFrame({'x': X, 'y': y[i]})
        lines = alt.Chart(df).mark_line().encode(
            x='x',
            y='y',
        )
        layered_lines.append(lines)
    
    # make final chart by layering
    p = alt.layer(*layered_lines)
    return p

def create_plotnine_graph(graph_object):
     # unpack data
    (X, y_layers, *_), styles = unpack_graph_object(graph_object)
    num_layers = len(y_layers)
    
    # create labels to group layers by
    layer_names = np.copy(y_layers)
    for i in range(num_layers):
        layer_names[i, :] = i

    # format data to be appropriate for a data frame
    X = np.append(X, [X] * (num_layers - 1))
    y_layers = y_layers.flatten()
    layer_names = convert_numbers_to_letters(layer_names.flatten())

    # create data frame
    df = pd.DataFrame({
        'X': X,
        'y': y_layers,
        'layer_names': layer_names
    })
    
    # make plot for each layer
    p = p9.ggplot(
        data=df, 
        mapping=p9.aes(
            x='X', 
            y='y', 
            color=layer_names,
        )
    ) + p9.geom_line(show_legend='None')

    return p