import numpy as np
import pandas as pd
import altair as alt
import plotnine as p9
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from utils.creators import unpack_graph_object
from utils.creators import convert_numbers_to_letters

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
        legend_label=convert_numbers_to_letters(layer_names),
    )
    
    # legend if applicable
    p.legend.visible = styles.get('show_legend')

    return p
    
def create_altair_graph(graph_object):
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
    y = y_layers.flatten()

    # create data frame
    df = pd.DataFrame({
        'X': X,
        'y': y,
        'layer_names': layer_names,
    })

    # assign legend if applicable 
    legend = alt.Legend(orient=styles.get('legend_position')) if styles.get('show_legend') else None

    # create area chart
    p = alt.Chart(df).mark_area().encode(
        x = alt.X('X', scale=alt.Scale(domain=[0, np.amax(X)], nice=False)),
        y = alt.Y('y:Q', stack='zero'),
        color = alt.Color('layer_names:N', scale=alt.Scale(range=styles.get('color')), legend=legend),
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
    # colors = np.array([[styles.get('color')[i]] * layer_names.shape[1] for i in range(layer_names.shape[0])]).flatten()

    for i in range(num_layers):
        layer_names[i, :] = i
    layer_names = convert_numbers_to_letters(layer_names.flatten())

    # format data to be appropriate for a data frame
    X = np.append(X, [X] * (num_layers - 1))
    y_layers = y_layers.flatten()
    data = pd.DataFrame({
        'X': X,
        'y': y_layers,
        'layer_names': layer_names,
    })
    
    # make plot for each layer
    p = (
        p9.ggplot(
            data=data, 
            mapping=p9.aes(
                x=X, 
                y=y_layers, 
                fill=layer_names,
            )
        )
        + p9.geom_area(show_legend=styles.get('show_legend'))
        + p9.labels.xlab('X')
        + p9.labels.ylab('y')
        + p9.theme(figure_size=(styles.get('width'), styles.get('height')))
        + p9.scale_fill_manual(values=styles.get('color'))
        + p9.labs(fill='Layers')
    )
        
    return p