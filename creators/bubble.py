import pandas as pd

from bokeh.plotting import show, figure
from bokeh.models import ColumnDataSource
from utils.creators import unpack_graph_object

import numpy as np
import altair as alt
import plotnine as p9

parameters = {
    'width': 400,
    'height': 400,
    'size': 10,
    'x_threshold': 0.05,
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y, bubble_size, *_), styles = unpack_graph_object(graph_object)

    # create dataframe  
    df = ColumnDataSource({
        'x': X,
        'y': y,
        'bubble_size': bubble_size,
    })
    
    # plot data points
    p = figure(
        width=parameters.get('width'),
        height=parameters.get('height'),
        x_axis_label='X',
        y_axis_label='y',
        toolbar_location=None,
    )
    p.scatter(
        x='x',
        y='y',
        size='bubble_size',
        fill_alpha=styles.get('opacity'),
        fill_color=styles.get('fill'),
        line_color=styles.get('color'),
        line_width=styles.get('stroke'),
        source=df
    )
    
    return p

def create_altair_graph(graph_object):
    # format data
    (X, y, bubble_size, *_), styles = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'X': X,
        'y': y,
        'size': bubble_size,
    })

    # create chart
    p = alt.Chart(df).mark_point().encode(
        x=alt.X('X', scale=alt.Scale(domain=calculate_axis_range(X, bubble_size))),
        y=alt.Y('y', scale=alt.Scale(domain=calculate_axis_range(y, bubble_size))),
        size=alt.Size('size', legend=None),
    ).configure_mark(
        opacity=styles.get('opacity'),
        color=styles.get('color'),
        filled=True,
    )

    return p

def create_plotnine_graph(graph_object):
    # format data
    (X, y, bubble_size, *_), styles = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'x': X,
        'y': y,
        'size': bubble_size,
    })

    # create plot
    p = p9.ggplot(
        data=df, 
        mapping=p9.aes(
            x='X', 
            y='y', 
            size='size',
        )
    ) + p9.geom_point(show_legend='None', fill=styles.get('fill'), color=styles.get('color'), stroke=styles.get('stroke'), alpha=styles.get('opacity')) + p9.labels.xlab('X') + p9.labels.ylab('y')
    
    return p

def calculate_axis_range(X, bubble_size):
    # percent_offset = np.amax(X) * parameters.get('x_threshold')
    # percent_offset = np.amax(X) * np.amax(bubble_size) * parameters.get('x_threshold')
    percent_offset = np.amax(X) * (np.amax(bubble_size)/100)
    # get height range
    height_range = (
        np.amin(X) - percent_offset,
        np.amax(X) + percent_offset,
    )
    return height_range