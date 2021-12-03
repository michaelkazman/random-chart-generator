import numpy as np
import altair as alt
import plotnine as p9
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from creators.utils import unpack_graph_object

parameters = {
    'width':    400,
    'height':   400,
    'colors': ['red', 'blue', 'green', 'orange', 'purple']
}

def create_bokeh_graph(graph_object):
    #unpack data
    X, y = graph_object['data']
    y = y.tolist()
    num_layers = len(y)    
    layer_names = [str(i) for i in range(num_layers)]

    # format dict with x and y such that y layers is labelled with ['y1', 'y2', ...]
    layers = { 'x': X }
    layers.update(dict([(str(index), layer) for index, layer in enumerate(y)]))

    # ensure each layer has a different color
    layer_colors = parameters['colors'][:num_layers]
    
    # create source
    df = ColumnDataSource(data=layers)
    
    # make figure
    p = figure(width=parameters['width'], height=parameters['height'])
    p.varea_stack(layer_names, x='x', source=df, color=layer_colors)

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
    df = pd.DataFrame({
        'x': X,
        'y': y,
        'layer_names': layer_names
    })

    # create area chart
    p = alt.Chart(df).mark_area().encode(
        x = 'x:T',
        y = 'y:Q',
        color = 'layer_names:N',
    ).properties(
        width=parameters['width'],
        height=parameters['height'],
    )
    return p

def create_plotnine_graph(graph_object):
    # unpack data
    (X, y_layers), style = unpack_graph_object(graph_object)
    num_layers = len(y_layers)
    
    # create labels to group layers by
    layer_names = np.copy(y_layers)
    for i in range(num_layers):
        layer_names[i, :] = i

    # format data to be appropriate for a data frame
    X = np.append(X, [X] * (num_layers - 1))
    y_layers = y_layers.flatten()
    layer_names = layer_names.flatten()

    layer_names = [chr(int(i)+65) for i in layer_names]

    data = pd.DataFrame({
        'X': X,
        'y': y_layers,
        'layer_names': layer_names
    })
    
    # make plot for each layer
    p = p9.ggplot(data=data, mapping=p9.aes(x=X, y=y_layers, fill=layer_names)) + p9.geom_area()
    
    return p