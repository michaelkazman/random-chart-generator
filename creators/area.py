import numpy as np
import pandas as pd
import altair as alt
import plotnine as p9
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from utils.creators import convert_numbers_to_letters, unpack_graph_object, generate_indices_list

def create_bokeh_graph(graph_object):
    #unpack data
    (X, y), styles = unpack_graph_object(graph_object)
    num_layers = len(y)    
    layer_names = convert_numbers_to_letters(range(num_layers))


    # format dict with x and y such that y layers is labelled with ['y1', 'y2', ...]
    layers = { 'X': X }
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

    # stack layers
    layer_indices = [str(i) for i in range(num_layers)]
    p.varea_stack(
        layer_indices, 
        x='X', 
        source=df, 
        color=styles.get('color'),
        legend_label=layer_names,
    )
    
    # render legend if applicable
    p.legend.title = styles.get('legend_title')
    p.legend.visible = styles.get('show_legend')

    return p
    
def create_altair_graph(graph_object):
    # unpack data
    (X, y_layers), styles = unpack_graph_object(graph_object)
    num_layers = len(y_layers)

    # create labels to group layers by
    layer_names = convert_numbers_to_letters(generate_indices_list(y_layers))

    # format data to be appropriate for a data frame
    X = np.append(X, [X] * (num_layers - 1))
    y = y_layers.flatten()

    # create data frame
    df = pd.DataFrame({
        'X': X,
        'y': y,
        'layer_names': layer_names,
    })

    # render legend if applicable 
    legend = alt.Legend(title=styles.get('legend_title'), orient=styles.get('legend_position')) if styles.get('show_legend') else None

    # create area chart
    p = alt.Chart(df).mark_area().encode(
        x = alt.X('X', scale=alt.Scale(domain=[np.amin(X), np.amax(X)], nice=False)),
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
    layer_names = convert_numbers_to_letters(generate_indices_list(y_layers))

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
        + p9.theme(figure_size=(styles.get('width'), styles.get('height')), legend_position=tuple(styles.get('legend_position')))
        + p9.scale_fill_manual(values=styles.get('color'))
        + p9.labs(fill=styles.get('legend_title'))
    )
        
    return p