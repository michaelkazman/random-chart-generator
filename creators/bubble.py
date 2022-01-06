import numpy as np
import pandas as pd
import altair as alt
import plotnine as p9
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from utils.creators import unpack_graph_object

def create_bokeh_graph(graph_object):
    # format data
    (X, y, bubble_size, *_), styles = unpack_graph_object(graph_object)

    # create dataframe  
    df = ColumnDataSource({
        'X': X,
        'y': y,
        'bubble_size': bubble_size,
    })
    
    # plot data points
    p = figure(
        width=styles.get('width'),
        height=styles.get('height'),
        x_axis_label='X',
        y_axis_label='y',
        toolbar_location=None,
    )
    p.scatter(
        x='X',
        y='y',
        size='bubble_size',
        fill_alpha=styles.get('opacity'),
        fill_color=styles.get('fill'),
        line_color=styles.get('stroke_color'),
        line_width=styles.get('stroke_width'),
        source=df,
    )
    
    return p

def create_altair_graph(graph_object):
    # format data
    (X, y, bubble_size, *_), styles = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'X': X,
        'y': y,
        'size': bubble_size,
    })

    # create chart
    p = alt.Chart(df).mark_point().encode(
        x=alt.X('X', scale=alt.Scale(domain=calculate_axis_range(X, bubble_size))),
        y=alt.Y('y', scale=alt.Scale(domain=calculate_axis_range(y, bubble_size))),
        size=alt.Size('size', legend=None),
    ).properties(
        width=styles.get('width'),
        height=styles.get('height'),
    ).configure_mark(
        opacity=styles.get('opacity'),
        fill=styles.get('fill'),
        stroke=styles.get('stroke_color'),
        strokeWidth=styles.get('stroke_width'),
        filled=True,
    )

    return p

def create_plotnine_graph(graph_object):
    # format data
    (X, y, bubble_size, *_), styles = unpack_graph_object(graph_object)
    df = pd.DataFrame({
        'x': X,
        'y': y,
        'size': bubble_size,
    })

    # create plot
    p = (
        p9.ggplot(data=df, mapping=p9.aes(x='X', y='y', size='size'))
        + p9.geom_point(
            show_legend='None',
            fill=styles.get('fill'),
            color=styles.get('stroke_color'),
            stroke=styles.get('stroke_width'),
            alpha=styles.get('opacity'),
        )
        + p9.labels.xlab('X')
        + p9.labels.ylab('y')
        + p9.theme(figure_size=(styles.get('width'), styles.get('height')))
    )
    
    return p

def calculate_axis_range(X, bubble_size):
    percent_offset = np.amax(X) * (np.amax(bubble_size)/100)

    height_range = (
        np.amin(X) - percent_offset,
        np.amax(X) + percent_offset,
    )
    return height_range