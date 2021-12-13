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
    'opacity': 0.5,
    'fill_color': '#084594',
    'line_color': '#084594',
    'x_threshold': 0.05,
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y, bubble_size, *_), style = unpack_graph_object(graph_object)

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
        toolbar_location=None,
    )
    p.scatter(
        x='x',
        y='y',
        size='bubble_size',
        fill_alpha=parameters.get('opacity'),
        fill_color= parameters.get('fill_color'),
        line_color=parameters.get('line_color'),
        source=df
    )
    
    return p

def create_altair_graph(graph_object):
    # format data
    (X, y, bubble_size, *_), style = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'X': X,
        'y': y,
        'size': bubble_size,
    })

    # create chart
    p = alt.Chart(df).mark_point().encode(
        x=alt.X('X', scale=alt.Scale(domain=calculate_axis_range(X, bubble_size))),
        # x=alt.X('X', scale=alt.Scale(domain=(np.amin(X), np.amax(X)))),
        y=alt.Y('y', scale=alt.Scale(domain=calculate_axis_range(y, bubble_size))),
        size=alt.Size('size', legend=None),
    )

    return p

def create_plotnine_graph(graph_object):
    # format data
    (X, y, bubble_size, *_), style = unpack_graph_object(graph_object)
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
    ) + p9.geom_point(show_legend='None')
    
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