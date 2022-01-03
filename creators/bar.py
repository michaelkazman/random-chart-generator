import pandas as pd
import altair as alt
import plotnine as p9
from bokeh.plotting import figure
from utils.creators import unpack_graph_object
from bokeh.models import ColumnDataSource, VBar, HBar

def create_bokeh_graph(graph_object):
    # format data
    (X, y, is_vertical, *_), styles = unpack_graph_object(graph_object)
    colors = styles.get('color') if styles.get('use_random_colors') else styles.get('color')[:1] * len(styles.get('color'))
    df = ColumnDataSource(dict(X=X, top=y, color=colors))

    # create plot
    p = figure(
        title=None,
        width=styles.get('width'),
        height=styles.get('height'),
        min_border=0,
        toolbar_location=None,
        x_axis_label='X',
        y_axis_label='y',
        x_range=X if is_vertical else None,
        y_range=X[::-1] if not is_vertical else None,
    )

    # create glyphs based on vertical or horizontal
    glyph = (
        VBar(
            x='X',
            top='top',
            bottom=0,
            width=styles.get('bar_width'),
            fill_color='color',
            line_width=styles.get('bar_width'),
        ) if is_vertical else HBar(
            y='X',
            right='top',
            left=0,
            height=styles.get('bar_width'),
            fill_color='color',
            line_width=styles.get('bar_width'),
        )
    )
    p.add_glyph(df, glyph)

    return p

def create_altair_graph(graph_object):
    # format data
    (X, y, is_vertical, *_), styles = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'x': X,
        'y': y,
    })

    # horizontal forces x to take the y values as quantitive
    encodings = { 'x': 'x:O', 'y': 'y:Q' } if is_vertical else { 'x': 'y:Q', 'y': 'x:O' }
    colors = styles.get('color') if styles.get('use_random_colors') else styles.get('color')[:1] * len(styles.get('color'))
    chart = alt.Chart(df).mark_bar(size=styles.get('bar_width')).encode(
        **encodings,
        color=alt.Color('y', scale=alt.Scale(range=colors), legend=None),
        size=styles.get('bar_width'),
    ).properties(
        width=styles.get('width'),
        height=styles.get('height'),
    )
    return chart

def create_plotnine_graph(graph_object):
    # format data
    (X, y, is_vertical, *_), styles = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'X': X,
        'y': y,
    })

    # create plot
    colors = styles.get('color') if styles.get('use_random_colors') else styles.get('color')[:1]
    p = (
        p9.ggplot(df, p9.aes(x='X', y='y'))
        + p9.geom_bar(
            stat='identity',
            mapping=p9.aes(fill=colors),
            show_legend=False,
            width=styles.get('bar_width'),
        )
        + p9.theme(figure_size=(styles.get('width'), styles.get('height')))
        + p9.scale_fill_manual(values=colors)
    )
    if not is_vertical: p += p9.coord_flip()

    return p