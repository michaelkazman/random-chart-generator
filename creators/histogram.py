import pandas as pd
import altair as alt

from bokeh.plotting import figure
from utils.creators import unpack_graph_object

parameters = {
    'width': 400,
    'height': 400,
    'alpha': 0.5,
}

def create_bokeh_graph(graph_object):
    # unpack data
    (X, y), style = unpack_graph_object(graph_object)

    # the x-coordinates of the left edges
    left_edges = y[:-1]
    right_edges = y[1:]

    # create plot
    p = figure(title=None, tools='')
    p.quad(top=X, bottom=0, left=left_edges, right=right_edges, alpha=parameters['alpha'])

    return p

def create_altair_graph(graph_object):
    # unpack data
    (X, y), style = unpack_graph_object(graph_object)
    
    # format data
    df = pd.DataFrame({
        'X': y[1:],
        'y': X, # set edges to right
    })

    # create histogram chart
    p = alt.Chart(df).mark_bar().encode(
        x='X',
        y='y',
    )

    return p


def create_plotnine_graph(graph_object):
    return {}