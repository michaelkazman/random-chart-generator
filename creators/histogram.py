import pandas as pd
import altair as alt
import plotnine as p9
from bokeh.plotting import figure
from utils.creators import unpack_graph_object

def create_bokeh_graph(graph_object):
    # unpack data
    (X, y, *_), styles = unpack_graph_object(graph_object)

    # the x-coordinates of the edges
    left_edges = X[:-1]
    right_edges = X[1:]
    color = [styles.get('color')] * len(y)

    # create plot
    p = figure(
        width=styles.get('width'),
        height=styles.get('height'),
        title=None,
        x_axis_label='X',
        y_axis_label='y',
        toolbar_location=None,
    )
    p.quad(
        top=y, 
        bottom=0, 
        left=left_edges, 
        right=right_edges, 
        color=color,
        alpha=styles.get('opacity'),
        line_width=styles.get('bar_width'),
    )

    return p

def create_altair_graph(graph_object):
    # unpack data
    (X, y, *_), styles = unpack_graph_object(graph_object)
    
    # format data
    df = pd.DataFrame({
        'X': X[:-1], # set edges to right
        'y': y,
    })

    # create histogram chart
    p = alt.Chart(df).mark_bar().encode(
        x='X',
        y='y',
    ).properties(
        width=styles.get('width'),
        height=styles.get('height'),
    ).configure_mark(
        color=styles.get('color'),
        opacity=styles.get('opacity'),
        size=styles.get('bar_width'),
    )

    return p

def create_plotnine_graph(graph_object):
    # unpack data, and set edges to right
    (X, y, *_), styles = unpack_graph_object(graph_object)
    X = X[:-1]

    # format data
    df = pd.DataFrame({
        'X': X, 
        'y': y, 
    })

    # create plot
    p = (
        p9.ggplot(df, p9.aes(x='X', y=p9.after_stat('y')))
        + p9.geom_histogram(bins=X.shape[0], fill=styles.get('color'), size=styles.get('bar_width'), alpha=styles.get('opacity'))
        + p9.theme(figure_size=(styles.get('width'), styles.get('height')))
    )

    return p