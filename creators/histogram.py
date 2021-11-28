from creators.utils import unpack_graph_object
from bokeh.plotting import figure
import altair as alt
import pandas as pd

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
    source = pd.DataFrame({
        'x': X[1:], # set edges to right
        'y': y,
    })

    # create histogram chart
    chart = alt.Chart(source).mark_bar().encode(
        x = 'x:O',
        y = 'y:Q',
    ).properties(
        width=parameters['width'],
        height=parameters['height'],
    )

    return chart


def create_plotnine_graph(graph_object):
    return {}