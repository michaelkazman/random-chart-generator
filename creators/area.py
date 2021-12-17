import numpy as np
import pandas as pd
import altair as alt
import plotnine as p9

from utils.creators import convert_numbers_to_letters
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from utils.creators import unpack_graph_object
from bokeh.io import curdoc

def create_bokeh_graph(graph_object):
    #unpack data
    (X, y), styles = unpack_graph_object(graph_object)
    y = y.tolist()
    num_layers = len(y)    
    layer_names = [str(i) for i in range(num_layers)]

    # format dict with x and y such that y layers is labelled with ['y1', 'y2', ...]
    layers = { 'x': X }
    layers.update(dict([(str(index), layer) for index, layer in enumerate(y)]))
    
    # create source
    df = ColumnDataSource(data=layers)

    # make figure
    p = figure(
        width=styles.get('width'),
        height=styles.get('height'),
        x_axis_label='X',
        y_axis_label='y',
        toolbar_location=None,
    )
    p.varea_stack(
        layer_names, 
        x='x', 
        source=df, 
        color=styles.get('color'),
    )

    return p
    
def create_altair_graph(graph_object):
    # unpack data
    (X, y_layers), styles = unpack_graph_object(graph_object)
    num_layers = len(y_layers)

    # create labels to group layers by
    layer_names = np.copy(y_layers)
    for i in range(num_layers):
        layer_names[i, :] = i
    layer_names = layer_names.flatten()

    # format data to be appropriate for a data frame
    X = np.append(X, [X] * (num_layers - 1))
    y = y_layers.flatten()

    # create data frame
    df = pd.DataFrame({
        'X': X,
        'y': y,
        'layer_names': layer_names,
    })

    # create area chart
    p = alt.Chart(df).mark_area().encode(
        x = alt.X('X', scale=alt.Scale(domain=[0, np.amax(X)], nice=False)),
        y = alt.Y('y:Q', stack='zero'),
        color = alt.Color('layer_names:N', legend=None),
    ).properties(
        width=styles.get('width'),
        height=styles.get('height'),
    )
    return p

def create_plotnine_graph(graph_object):
    # unpack data
    (X, y_layers), styles = unpack_graph_object(graph_object)
    num_layers = len(y_layers)
    
    # create labels to group layers by
    layer_names = np.copy(y_layers)
    for i in range(num_layers):
        layer_names[i, :] = i
    layer_names = convert_numbers_to_letters(layer_names.flatten())

    # format data to be appropriate for a data frame
    X = np.append(X, [X] * (num_layers - 1))
    y_layers = y_layers.flatten()

    data = pd.DataFrame({
        'X': X,
        'y': y_layers,
        'layer_names': layer_names
    })
    
    # make plot for each layer
    p = (
        p9.ggplot(data=data, mapping=p9.aes(x=X, y=y_layers, fill=layer_names))
        + p9.geom_area(show_legend=False)
        + p9.labels.xlab('X')
        + p9.labels.ylab('y')
    )
        
    return p