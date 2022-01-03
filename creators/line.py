import numpy as np
import pandas as pd
import altair as alt
import plotnine as p9
from bokeh.plotting import figure
from utils.creators import convert_numbers_to_letters, unpack_graph_object

def create_bokeh_graph(graph_object):
    # unpack data
    (X, y, *_), styles = unpack_graph_object(graph_object)
    num_layers = len(y)    
    layer_names = convert_numbers_to_letters([str(i) for i in range(num_layers)])

    # create plot
    p = figure(
        width=styles.get('width'),
        height=styles.get('height'),
        x_axis_label='X',
        y_axis_label='y',
        toolbar_location=None,
    )
    
    # draw each line individually
    for i, y_list in enumerate(y):
        p.line(X, y_list, color=styles.get('color')[i], legend_label=layer_names[i])
        getattr(p, styles.get('marker_type'))(X, y_list, color=styles.get('color')[i], size=styles.get('marker_size'))
    
    # legend if applicable
    p.legend.visible = styles.get('show_legend')
    
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
            color = alt.value(styles.get('color')[i]),
        ).properties(
            height = styles.get('height'),
            width = styles.get('width'),
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
        'layer_names': layer_names,
    })
    
    # make plot for each layer
    p = (
        p9.ggplot(
            data=df, 
            mapping=p9.aes(
                x='X', 
                y='y', 
                color=layer_names,
                fill=layer_names,
            ),
        ) 
        + p9.geom_line(show_legend=styles.get('show_legend'))
        + p9.theme(figure_size=(styles.get('width'), styles.get('height')))
        + p9.scale_color_manual(values=styles.get('color'))
        + p9.scale_fill_manual(values=styles.get('color'))
        + p9.labs(color="Layer Names")
    )

    return p