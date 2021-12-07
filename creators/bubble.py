import pandas as pd

from bokeh.plotting import show, figure
from bokeh.models import ColumnDataSource
from utils.creators import unpack_graph_object

import altair as alt
import plotnine as p9

parameters = {
    'width': 400,
    'height': 400,
    'size': 10,
    'opacity': 0.5,
    'fill_color': '#084594',
    'line_color': '#084594',
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y, bubble_size), style = unpack_graph_object(graph_object)

    # create dataframe  
    df = ColumnDataSource({
        'x': X,
        'y': y,
        'bubble_size': bubble_size,
    })
    
    # plot data points
    p = figure(
        width=parameters.get('width'),
        height=parameters.get('height')
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
    (X, y, bubble_size), style = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'x': X,
        'y': y,
        'size': bubble_size,
    })

    # create chart
    p = alt.Chart(df).mark_point().encode(
        x='x',
        y='y',
        size='size'
    )

    return p

def create_plotnine_graph(graph_object):
    # format data
    (X, y, bubble_size), style = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'x': X,
        'y': y,
        'size': bubble_size,
    })

    # create plot
    p = p9.ggplot(data=df, mapping=p9.aes(x='X', y='y', size='size')) + p9.geom_point()
    
    return p