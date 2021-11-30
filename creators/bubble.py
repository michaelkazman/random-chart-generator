from creators.utils import unpack_graph_object
import pandas as pd
from bokeh.plotting import show, figure
from bokeh.models import ColumnDataSource

parameters = {
    'width': 400,
    'height': 400,
    'size': 10,
    'opacity': 0.5,
    'fill_color': "#084594",
    'line_color': "#084594",
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y, bubble_size), style = unpack_graph_object(graph_object)

    # create dataframe  
    df = pd.DataFrame(data={
        'x': X,
        'y': y,
        'bubble_size': bubble_size,
    })
    source = ColumnDataSource(df)
    
    # plot data points
    p = figure(
        width=parameters['width'],
        height=parameters['height']
    )
    p.scatter(
        x='x',
        y='y',
        size='bubble_size',
        fill_alpha=parameters['opacity'],
        fill_color= parameters['fill_color'],
        line_color=parameters['line_color'],
        source=source
    )
    
    return p

def create_altair_graph(graph_object):
    return {}

def create_plotnine_graph(graph_object):
    return {}