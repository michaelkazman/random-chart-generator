import numpy as np
import pandas as pd
import plotnine as p9
import altair as alt
from utils.creators import unpack_graph_object
from bokeh.plotting import figure
from utils.creators import convert_numbers_to_letters, unpack_graph_object

def create_bokeh_graph(graph_object):
    (X, y, *_), styles = unpack_graph_object(graph_object)

    p = figure(
        toolbar_location=None,
        width = styles.get('width'),
        height = styles.get('height'),
    )
    for i in range(X.shape[0]):
        p.line(
            X[i],
            y[i], 
            line_color=styles.get('color')[i], 
            line_width=styles.get('line_thickness'), 
            alpha=0.7,
        )

    p.y_range.start = 0
    p.xaxis.axis_label = 'x'
    p.yaxis.axis_label = 'Pr(x)'
    p.grid.grid_line_color="white"

    return p

def create_altair_graph(graph_object):
    # unpack data
    (X, y, *_), styles = unpack_graph_object(graph_object)

    # for each layer, make data frame and store its line graph
    layered_lines = []
    for i in range(X.shape[0]):
        df = pd.DataFrame({'x': X[i], 'y': y[i]})
        lines = alt.Chart(df).mark_line().encode(
            x='x',
            y='y',
            color=alt.value(styles.get('color')[i]),
            strokeWidth=alt.value(styles.get('line_thickness')),
        ).properties(
            width=styles.get('width'),
            height=styles.get('height'),
        )
        
        layered_lines.append(lines)
    
    # make final chart by layering
    p = alt.layer(*layered_lines)
    return p

def create_plotnine_graph(graph_object):
     # unpack data
    (X, y, *_), styles = unpack_graph_object(graph_object)
    num_layers = X.shape[0]
    
    # create labels to group layers by
    layer_names = np.copy(y)
    for i in range(num_layers):
        layer_names[i, :] = i    

    # format data to be appropriate for a data frame
    X = X.flatten()
    y = y.flatten()
    layer_names = convert_numbers_to_letters(layer_names.flatten())

    # create data frame
    df = pd.DataFrame({
        'X': X,
        'y': y,
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
            )
        ) 
        + p9.geom_line(show_legend='None', size=styles.get('line_thickness')) 
        + p9.scale_color_manual(values=styles.get('color'))
        + p9.scale_fill_manual(values=styles.get('color'))
        + p9.theme(figure_size=(styles.get('width'), styles.get('height')))
    )

    return p