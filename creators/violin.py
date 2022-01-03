import numpy as np
import pandas as pd
import altair as alt
import plotnine as p9
import holoviews as hv
import hvplot.pandas # needed for rendering bokeh violin plots
from holoviews import opts
from utils.creators import unpack_graph_object

# set holoviews to use bokeh
hv.extension('bokeh')

parameters = {
    'color': 'black',
    'orientation': 'horizontal',
    'stack': 'center',
    'resolve_mode': 'independent',
    'bokeh_height_min_threshold': 1.5,
    'bokeh_height_max_threshold': 1.5,
    'height_min_threshold': 1,
    'height_max_threshold': 1,
    'padding': 20,
}

def create_bokeh_graph(graph_object):
    # format data
    (X, y), styles = unpack_graph_object(graph_object)
    data = pd.DataFrame({
        'X': X,
        'y': y,
    })

    # create holoviews plot
    p = data.hvplot.violin(
        width=styles.get('width'), 
        height=styles.get('height'), 
        y='y',
        by='X',
        c='X',
        legend=False, 
    ).opts(opts.Violin(
        ylim=calculate_y_lim(y, ['bokeh_height_min_threshold', 'bokeh_height_max_threshold']),
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
    y_limit = calculate_y_lim(y)
    violin = alt.Chart().transform_density(
        'y',
        as_=['y', 'density'],
        extent=y_limit,
        groupby=['X'],
    ).mark_area(orient='horizontal').encode(
        y='y:Q',
        color=alt.Color('X:N', legend=None),
        x=alt.X(
            'density:Q',
            stack='center',
            impute=None,
            title=None,
            scale=alt.Scale(nice=False, zero=False, padding=parameters.get('padding')),
            axis=alt.Axis(labels=False, values=[0], grid=False, ticks=True),
        ),
    ).properties(
        width=styles.get('width'),
        height=styles.get('height'),
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
    p = (
        p9.ggplot(df, p9.aes(x='X', y='y'))
        + p9.geom_violin()
        + p9.geom_boxplot(width=0.1)
        + p9.theme(figure_size=(styles.get('width'), styles.get('height')))
    )

    return p

def calculate_y_lim(y, threshold_names=['height_min_threshold', 'height_max_threshold']):
    # get height range
    height_range = (
        np.min(y) * (1 + parameters.get(threshold_names[0], 0)),
        np.max(y) * (1 + parameters.get(threshold_names[1], 0))
    )
    return height_range