import pandas as pd
import altair as alt
import plotnine as p9

from bokeh.plotting import figure
from utils.creators import unpack_graph_object
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Scatter

parameters = {
    'width': 300,
    'height': 300,
    'bokeh_size': 6,
    'altair_size': 60, # basically bokeh_size * 10
    'marker_type' : 'circle',
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y, *_), styles = unpack_graph_object(graph_object)
    df = ColumnDataSource(dict(x=X, y=y))

    # create plot
    p = figure(
        title=None,
        width=parameters.get('width'),
        height=parameters.get('height'),
        x_axis_label='X',
        y_axis_label='y',
        min_border=0,
        toolbar_location=None,
    )

    # create glyph (symbol for plotting data points)
    glyph = Scatter(
        x='x',
        y='y',
        size=parameters.get('bokeh_size'),
        marker=parameters.get('marker_type')
    )
    p.add_glyph(df, glyph)

    return p

def create_altair_graph(graph_object):
    # format data
    (X, y, *_), styles = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'X': X,
        'y': y,
    })

    # create scatterplot
    p = alt.Chart(df).mark_circle(
        size=parameters.get('altair_size')
    ).encode(
        x='X',
        y='y',
    ).properties(
        width=parameters.get('width'),
        height=parameters.get('height'),
    ) 

    return p

def create_plotnine_graph(graph_object):
    # format data
    (X, y, *_), styles = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'X': X,
        'y': y,
    })

    # create plot
    p = p9.ggplot(data=df, mapping=p9.aes(x='X', y='y')) + p9.geom_point()
    
    return p