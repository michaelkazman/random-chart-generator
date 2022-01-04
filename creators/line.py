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
    num_layers = len(y)

    # create labels to group layers by
    layer_names = np.copy(y)
    for i in range(num_layers):
        layer_names[i, :] = i
    layer_names = convert_numbers_to_letters(layer_names.flatten())

    # format data to be appropriate for a data frame
    X = np.append(X, [X] * (num_layers - 1))
    y = y.flatten()

    # create data frame
    df = pd.DataFrame({
        'X': X,
        'y': y,
        'layer_names': layer_names,
    })

    # assign legend if applicable 
    legend = alt.Legend(orient=styles.get('legend_position')) if styles.get('show_legend') else None

    # create line chart
    p = alt.Chart(df).mark_line().encode(
        x=alt.X('X', scale=alt.Scale(domain=[0, np.amax(X)], nice=False)),
        y=alt.Y('y:Q'),
        color= alt.Color('layer_names:N', scale=alt.Scale(range=styles.get('color')), legend=legend),
    ).properties(
        width=styles.get('width'),
        height=styles.get('height'),
    )

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
        + p9.labs(color='Layers')
    )

    return p