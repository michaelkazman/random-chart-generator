import pandas as pd
import altair as alt
import plotnine as p9
from bokeh.plotting import figure
from utils.creators import unpack_graph_object
from bokeh.models import ColumnDataSource, Scatter

def create_bokeh_graph(graph_object):
    # format data
    (X, y, *_), styles = unpack_graph_object(graph_object)
    df = ColumnDataSource(dict(X=X, y=y))

    # create plot
    p = figure(
        title=None,
        width=styles.get('width'),
        height=styles.get('height'),
        x_axis_label='X',
        y_axis_label='y',
        min_border=0,
        toolbar_location=None,
    )

    # create glyph (symbol for plotting data points)
    glyph = Scatter(
        x='X',
        y='y',
        size=styles.get('size'),
        marker=styles.get('type'),
        fill_alpha=styles.get('opacity'),
        fill_color=styles.get('color'),
        line_color=styles.get('stroke_color'),
        line_width=styles.get('stroke_width'),
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
        size=styles.get('size'),
        fill=styles.get('color'),
        opacity=styles.get('opacity'),
        stroke=styles.get('stroke_color'),
        strokeWidth=styles.get('stroke_width'),
    ).encode(
        x='X',
        y='y',
    ).properties(
        width=styles.get('width'),
        height=styles.get('height'),
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
    p = (
        p9.ggplot(data=df, mapping=p9.aes(x='X', y='y'))
        + p9.geom_point(
            show_legend='None',
            fill=styles.get('color'),
            alpha=styles.get('opacity'),
            color=styles.get('stroke_color'),
            stroke=styles.get('stroke_width'),
            size=styles.get('size'),
        )
        + p9.theme(figure_size=(styles.get('width'), styles.get('height')))
    )
    
    return p