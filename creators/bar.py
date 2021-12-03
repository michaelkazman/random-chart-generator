import pandas as pd
import altair as alt

from bokeh.io import curdoc
from creators.utils import unpack_graph_object
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, VBar, HBar

parameters = {
    'width': 300,
    'height': 300,
    'bar_width': 0.5,
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y, is_vertical), style = unpack_graph_object(graph_object)
    df = ColumnDataSource(dict(X=X, top=y))

    # create plot
    p = Plot(
        title=None,
        width=parameters['width'],
        height=parameters['height'],
        min_border=0,
        toolbar_location=None
    )

    # create glyphs based on vertical or horizontal
    glyph = (VBar(x='X', top='top', bottom=0, width=parameters['bar_width']) if is_vertical
        else HBar(y='X', right='top', left=0, height=parameters['bar_width']))
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
    (X, y, is_vertical), style = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'x': X,
        'y': y,
    })

    # horizontal forces x to take the y values as quantitive
    encodings = { 'x': 'x:O', 'y': 'y:Q' } if is_vertical else { 'x': 'y:Q', 'y': 'x:O' }
    
    chart = alt.Chart(df).mark_bar().encode(
        **encodings
    ).properties(
        width=parameters['width'],
        height=parameters['height'],
    )
    return chart

def create_plotnine_graph(graph_object):
    # format data
    (X, y, is_vertical), style = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'X': X,
        'y': y,
    })

    # create plot
    p = p9.ggplot(df, p9.aes(x='X', y='y')) + p9.geom_bar(stat='identity') 
    if not is_vertical: p += p9.coord_flip()

    return p