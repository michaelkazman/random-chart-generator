import numpy as np
import altair as alt
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from creators.utils import unpack_graph_object

parameters = {
    'width':    400,
    'height':   400,
    'colours': ['red', 'blue', 'green', 'orange', 'purple']
}

def create_bokeh_graph(graph_object):
    #unpack data
    X, y = graph_object['data']

    # make y a list
    y = y.tolist()

    # format dict with x and y such that y layers is labelled with ['y1', 'y2', ...]
    layers = {'x': X}
    for index, layer in enumerate(y):
        layers[str(index)] = layer
    num_layers = len(y)    
    layer_names = [str(i) for i in range(num_layers)]

    # ensure each layer has a different colour
    layer_colours = parameters['colours'][:num_layers]
    
    # create source
    source = ColumnDataSource(data=layers)
    
    # make figure
    p = figure(width=parameters['width'], height=parameters['height'])
    p.varea_stack(layer_names, x='x', source=source, color=layer_colours)

    show(p)
    return p
    
def create_altair_graph(graph_object):
    # unpack data
    (X, y_layers), style = unpack_graph_object(graph_object)
    num_layers = len(y_layers)

    # create labels to group layers by
    layer_names = np.copy(y_layers)
    for i in range(num_layers):
        layer_names[i, :] = str(i)

    # format data to be appropriate for a data frame
    X = np.append(X, [X] * (num_layers - 1))
    y = y_layers.flatten()
    layer_names = layer_names.flatten()
    
    # create data frame
    source = pd.DataFrame({
        'x': X,
        'y': y,
        'layer_names': layer_names
    })

    # create histogram chart
    chart = alt.Chart(source).mark_area().encode(
        x = 'x:T',
        y = 'y:Q',
        color = 'layer_names:N',
    ).properties(
        width=parameters['width'],
        height=parameters['height'],
    )
    return chart

def create_plotnine_graph(graph_object):
    return {}