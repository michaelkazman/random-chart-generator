import numpy as np
import pandas as pd
import altair as alt
import plotnine as p9
import holoviews as hv
import hvplot.pandas # needed for rendering bokeh violin plots
from holoviews import opts
from collections import Counter
from utils.creators import unpack_graph_object

# set holoviews to use bokeh
hv.extension('bokeh')

def create_bokeh_graph(graph_object):
    # format data
    (X, y), styles = unpack_graph_object(graph_object)
    data = pd.DataFrame({
        'X': X,
        'y': y,
    })

    # create holoviews plot
    colors = styles.get('color') if styles.get('use_random_colors') else styles.get('color')[:1] * len(styles.get('color'))
    p = data.hvplot.violin(
        y='y',
        by='X',
        c='X',
        legend=False, 
    ).opts(opts.Violin(
        width=styles.get('width'),
        height=styles.get('height'),
        ylim=calculate_y_lim(y, styles.get('min_height_threshold'), styles.get('max_height_threshold')),
        cmap=colors
    ))

    # turn plot into bokeh plot, and set toolbar to autohide
    p = hv.render(p, backend='bokeh')
    p.toolbar.autohide = True

    return p

def create_altair_graph(graph_object):
    # format data
    (X, y), styles = unpack_graph_object(graph_object)
    
    # create boxplot
    boxplot = alt.Chart().mark_boxplot(color='black').encode(
        alt.Y('y:Q'),
    ).properties(width=200)

    # create violin
    colors = styles.get('color') if styles.get('use_random_colors') else styles.get('color')[:1] * len(styles.get('color'))
    y_limit = calculate_y_lim(y, styles.get('min_height_threshold'), styles.get('max_height_threshold'))
    violin = alt.Chart().transform_density(
        'y',
        as_=['y', 'density'],
        extent=y_limit,
        groupby=['X'],
    ).mark_area(orient='horizontal').encode(
        y='y:Q',
        fill=alt.Color('X:N', scale=alt.Scale(range=colors), legend=None),
        color=alt.Color('X:N', scale=alt.Scale(range=colors), legend=None),
        x=alt.X(
            'density:Q',
            stack='center',
            impute=None,
            title=None,
            scale=alt.Scale(nice=False, zero=False, padding=styles.get('padding')),
            axis=alt.Axis(labels=False, values=[0], grid=False, ticks=True),
        ),
    ).properties(
        width=(styles.get('width') / len(styles.get('color'))),
        height=(styles.get('height')),
    )

    # stack violin with inner boxplot
    facet = lambda data: alt.layer(
        violin,
        boxplot,
        data=data,
    ).facet(
        column='X:N',
    ).resolve_scale(
        x=alt.ResolveMode('independent'),
    )


    # plot the layered violin and boxplots from above
    # puts layered graphs into a facet for plotting
    df = pd.DataFrame({ 'X': X, 'y': y, })
    plot = alt.hconcat(facet(df), spacing=40).configure_facet(
        spacing=0,
    ).configure_header(
        titleOrient='bottom',
        labelOrient='bottom',
    ).configure_view(
        stroke=None,
    )

    return plot

def create_plotnine_graph(graph_object):
    # unpack data
    (X, y), styles = unpack_graph_object(graph_object)

    # create data frame
    df = pd.DataFrame({
        'X': X,
        'y': y,
    })

    # create plot
    colors = styles.get('color') if styles.get('use_random_colors') else styles.get('color')[:1] * len(styles.get('color'))
    p = (
        p9.ggplot(df, p9.aes(x='X', y='y', fill=X))
        + p9.geom_violin(show_legend=False)
        + p9.geom_boxplot(width=0.1, fill='black')
        + p9.theme(figure_size=(styles.get('width'), styles.get('height')))
        + p9.scale_fill_manual(values=colors)
    )

    return p

def calculate_y_lim(y, min_threshold, max_threshold):
    # get height range
    height_range = (
        np.min(y) * (1 + min_threshold),
        np.max(y) * (1 + max_threshold),
    )
    return height_range