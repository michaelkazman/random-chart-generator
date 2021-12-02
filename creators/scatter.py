from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Scatter
from creators.utils import unpack_graph_object
import altair as alt
import pandas as pd

parameters = {
    'width': 300,
    'height': 300,
    'bokeh_size': 6,
    'altair_size': 60, # basically bokeh_size * 10
    'marker_type' : 'circle',
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y), style = unpack_graph_object(graph_object)
    df = ColumnDataSource(dict(x=X, y=y))

    # create plot
    p = Plot(
        title=None,
        width=parameters['width'],
        height=parameters['height'],
        min_border=0, toolbar_location=None
    )

    # create glyph (symbol for plotting data points)
    glyph = Scatter(x='x', y='y', size=parameters['bokeh_size'], marker=parameters['marker_type'])
    p.add_glyph(df, glyph)

    # adjust axes
    xaxis, yaxis = LinearAxis(), LinearAxis()
    p.add_layout(xaxis, 'below')
    p.add_layout(yaxis, 'left')

    # cosmetic adjustments (makes graph look more elegant)
    p.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    p.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

    return p

def create_altair_graph(graph_object):
    # format data
    (X, y), style = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'x': X,
        'y': y,
    })

    # create scatterplot
    p = alt.Chart(df).mark_circle(
        size=parameters['altair_size']
    ).encode(
        x='x',
        y='y',
    ).properties(
        width=parameters['width'],
        height=parameters['height'],
    ) 

    return p

def create_plotnine_graph(graph_object):
    return {}